from typing import Any, List
from uuid import UUID

from PyQt5.QtCore import (
    QAbstractListModel,
    QItemSelectionModel,
    QModelIndex,
    QRect,
    QSize,
    Qt,
    pyqtSignal,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QListView,
    QStyle,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
)

from musa.manager import ResourceManager
from musa.model.frame import Frame
from musa.model.sprite import Sprite
from musa.widget.button import IconButton


class SpriteListModel(QAbstractListModel):
    def __init__(self, frame: Frame, parent=None):
        super().__init__(parent)
        self.frame = frame
        self.sprites: List[UUID] = []

    def _refresh_sprite_list(self):
        self.sprites = [s.id for s in self.frame.sprites]

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self.sprites)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < len(self.sprites):
            return None

        sprite = self.frame.get_sprite(self.sprites[index.row()])

        if role == Qt.DisplayRole:
            return sprite.name
        elif role == Qt.UserRole:
            return sprite.visible
        elif role == Qt.UserRole + 1:
            return sprite  # Store the sprite object

        return None

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole):
        if not index.isValid() or not 0 <= index.row() < len(self.sprites):
            return False

        if role == Qt.UserRole:  # For visibility updates
            id = self.sprites[index.row()]
            self.frame.get_sprite(id).visible = value

            self.dataChanged.emit(index, index, [role])
            return True

        return False

    def move_sprite(self, from_index: int, to_index: int):
        self.frame.move_sprite(self.sprites[from_index], self.sprites[to_index])

        self.beginResetModel()
        self._refresh_sprite_list()
        self.endResetModel()

    def set_current_frame(self, frame: Frame):
        self.beginResetModel()
        self.frame = frame
        self._refresh_sprite_list()
        self.endResetModel()


class SpriteItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.visible = ResourceManager.get_scaled_pixmap("eye", 16)
        self.hidden = ResourceManager.get_scaled_pixmap("eye_off", 16)

    def sizeHint(self, option, index):
        return QSize(150, 30)

    def icon_rect(self, rect: QRect, pixmap: QPixmap, offset_x: int = 0) -> QRect:
        icon_rect = QRect(rect)
        icon_rect.setWidth(pixmap.width())
        icon_rect.setHeight(pixmap.height())

        padding = 12

        # Center the icon in the painter rectangle
        x = (rect.width() - (icon_rect.width() + padding)) - offset_x
        y = (rect.height() - icon_rect.height()) // 2

        return icon_rect.translated(x, y)

    def paint(self, painter, option, index: QModelIndex):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Draw the sprite name
        painter.drawText(
            option.rect.adjusted(5, 5, -40, -5),
            Qt.AlignVCenter | Qt.AlignLeft,
            index.data(Qt.DisplayRole),
        )

        # Draw the visibility icon
        visible = index.data(Qt.UserRole)
        icon = self.visible if visible else self.hidden
        painter.drawPixmap(
            self.icon_rect(option.rect, icon),
            icon,
        )

    def editorEvent(self, event, model, option, index):
        if event.type() == event.MouseButtonRelease:
            icon_rect = self.icon_rect(option.rect, self.visible)
            if icon_rect.contains(event.pos()):
                current_visibility = index.data(Qt.UserRole)
                model.setData(index, not current_visibility, Qt.UserRole)
                return True
        return False


class SpriteListWidget(QWidget):
    spriteSelected = pyqtSignal(Sprite)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame: Frame = None
        self.sprite_model = SpriteListModel(self.frame)

        self.setup_ui()

        self.list.setModel(self.sprite_model)
        self.list.setItemDelegate(SpriteItemDelegate())

        self.connections()

    def connections(self):
        self.list.selectionModel().currentChanged.connect(self._on_sprite_selected)

        self.up_btn.clicked.connect(self._move_sprite_up)
        self.down_btn.clicked.connect(self._move_sprite_down)
        self.del_btn.clicked.connect(self._on_sprite_remove)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        sprite_group = QGroupBox("Sprites")
        sprite_group_lay = QHBoxLayout()

        self.list = QListView()
        sprite_group_lay.addWidget(self.list)

        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignTop)

        self.up_btn = IconButton(ResourceManager.get_icon("arrow_up"))
        self.down_btn = IconButton(ResourceManager.get_icon("arrow_down"))
        self.del_btn = IconButton(ResourceManager.get_icon("delete_bin"))

        # Disable buttons by default
        self.del_btn.setEnabled(False)
        self.up_btn.setEnabled(False)
        self.down_btn.setEnabled(False)

        btn_layout.addWidget(self.del_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.up_btn)
        btn_layout.addWidget(self.down_btn)

        sprite_group_lay.addLayout(btn_layout)
        sprite_group.setLayout(sprite_group_lay)
        layout.addWidget(sprite_group)
        self.setLayout(layout)

    def set_frame(self, frame: Frame):
        self.frame = frame
        self.sprite_model.set_current_frame(self.frame)

    def _on_sprite_selected(self, current: QItemSelectionModel):
        self._update_buttons(current)

        if not current.isValid():
            self.spriteSelected.emit(None)
            return

        sprite = current.data(Qt.UserRole + 1)
        self.spriteSelected.emit(sprite)

    def _update_buttons(self, current: QItemSelectionModel):
        enabled = current.isValid()
        row = current.row() if enabled else -1
        row_count = self.sprite_model.rowCount()

        self.up_btn.setEnabled(enabled and row > 0)
        self.down_btn.setEnabled(enabled and row < row_count - 1)
        self.del_btn.setEnabled(enabled)

    def _move_sprite_up(self):
        current = self.list.currentIndex()
        if not current.isValid() or current.row() <= 0:
            return

        self.sprite_model.move_sprite(current.row(), current.row() - 1)
        self.list.setCurrentIndex(self.sprite_model.index(current.row() - 1, 0))

    def _move_sprite_down(self):
        current = self.list.currentIndex()
        if not current.isValid() or current.row() >= self.sprite_model.rowCount() - 1:
            return

        self.sprite_model.move_sprite(current.row(), current.row() + 1)
        self.list.setCurrentIndex(self.sprite_model.index(current.row() + 1, 0))

    def _on_sprite_remove(self):
        pass
