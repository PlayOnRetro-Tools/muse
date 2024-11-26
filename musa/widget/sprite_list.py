from PyQt5.QtCore import QAbstractListModel, QModelIndex, QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QStyle,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
)

from musa.model.animation_collection import AnimationCollection
from musa.model.frame import Frame
from musa.model.sprite import Sprite


class SpriteListModel(QAbstractListModel):
    def __init__(self, data_model: AnimationCollection, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.current_animation = -1
        self.current_frame = -1

    def rowCount(self, parent=QModelIndex()):
        return 0
        if self.current_animation < 0 or self.current_frame < 0:
            return 0

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or self.current_animation < 0 or self.current_frame < 0:
            return None

        sprite = self.data_model.get_sprites(
            self.current_animation, self.current_frame
        )[index.row()]

        if role == Qt.DisplayRole:
            return sprite.name
        elif role == Qt.UserRole:  # Use UserRole to store visibility
            return sprite.visible
        elif role == Qt.UserRole + 1:  # Store the entire sprite object
            return sprite

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or self.current_animation < 0 or self.current_frame < 0:
            return False

        if role == Qt.UserRole:  # For visibility updates
            self.data_model.set_sprite_visibility(
                self.current_animation, self.current_frame, index.row(), value
            )
            self.dataChanged.emit(index, index, [role])
            return True

        return False

    def move_sprite(self, from_index, to_index):
        """Move sprite in the z-order"""
        if from_index < 0 or to_index < 0:
            return False

        success = self.data_model.move_sprite(
            self.current_animation, self.current_frame, from_index, to_index
        )

        if success:
            self.beginResetModel()  # Reset model to reflect new order
            self.endResetModel()
        return success

    def set_current_frame(self, animation_index, frame_index):
        self.beginResetModel()
        self.current_animation = animation_index
        self.current_frame = frame_index
        self.endResetModel()


class SpriteItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        return QSize(200, 40)

    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Draw the sprite name
        painter.drawText(
            option.rect.adjusted(5, 5, -40, -5),
            Qt.AlignVCenter | Qt.AlignLeft,
            index.data(Qt.DisplayRole),
        )

        # Draw visibility icon
        visible = index.data(Qt.UserRole)
        icon_text = "👁️" if visible else "''👁️‍🗨️"
        painter.drawText(
            option.rect.adjusted(option.rect.width() - 35, 5, -5, -5),
            Qt.AlignVCenter | Qt.AlignRight,
            icon_text,
        )

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonRelease:
            icon_rect = option.rect.adjusted(option.rect.width() - 35, 5, -5, -5)
            if icon_rect.contains(event.pos()):
                current_visibility = index.data(Qt.UserRole)
                model.setData(index, not current_visibility, Qt.UserRole)
                return True
        return False


class SpriteListWidget(QWidget):
    spriteSelected = pyqtSignal(object)

    def __init__(self, frame=None, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.data_model = frame
        self.sprite_model = SpriteListModel(self.data_model)
        self.list.setModel(self.sprite_model)
        self.list.setItemDelegate(SpriteItemDelegate())

        self.list.selectionModel().currentChanged.connect(self._on_sprite_selected)

        # Buttons
        self.up_btn.clicked.connect(self._move_sprite_up)
        self.down_btn.clicked.connect(self._move_sprite_down)
        self.del_btn.clicked.connect(self._on_sprite_remove)

    def setup_ui(self):
        layout = QVBoxLayout()

        title_lay = QHBoxLayout()
        self.title = QLabel("Sprites")
        title_lay.addWidget(self.title)

        list_lay = QVBoxLayout()
        self.list = QListView()
        list_lay.addWidget(self.list)

        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignTop)
        self.up_btn = QPushButton("↑")
        self.down_btn = QPushButton("↓")
        self.del_btn = QPushButton("-")
        self.up_btn.setFixedSize(32, 32)
        self.down_btn.setFixedSize(32, 32)
        self.del_btn.setFixedSize(32, 32)

        # Disable reorder buttons by default
        self.up_btn.setEnabled(False)
        self.down_btn.setEnabled(False)

        btn_layout.addWidget(self.del_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.up_btn)
        btn_layout.addWidget(self.down_btn)

        hbox = QHBoxLayout()
        hbox.addLayout(list_lay)
        hbox.addLayout(btn_layout)

        layout.addLayout(title_lay)
        layout.addLayout(hbox)

        self.setLayout(layout)

    def _on_sprite_selected(self, current, previous):
        self._update_reorder_buttons(current)

        if not current.isValid():
            self.properties_widget.update_sprite(None)
            return

        sprite = current.data(Qt.UserRole + 1)
        self.spriteSelected.emit(sprite)

    def _update_reorder_buttons(self, current):
        """Enable/disable reorder buttons based on current selection"""
        enabled = current.isValid()
        row = current.row() if enabled else -1
        row_count = self.sprite_model.rowCount()

        self.up_btn.setEnabled(enabled and row > 0)
        self.down_btn.setEnabled(enabled and row < row_count - 1)

    def _move_sprite_up(self):
        current = self.list.currentIndex()
        if not current.isValid() or current.row() <= 0:
            return

        self.sprite_model.move_sprite(current.row(), current.row() - 1)
        self.sprites_view.setCurrentIndex(self.sprite_model.index(current.row() - 1, 0))

    def _move_sprite_down(self):
        current = self.list.currentIndex()
        if not current.isValid() or current.row() >= self.sprite_model.rowCount() - 1:
            return

        self.sprite_model.move_sprite(current.row(), current.row() + 1)
        self.sprites_view.setCurrentIndex(self.sprite_model.index(current.row() + 1, 0))

    def _on_sprite_remove(self):
        pass
