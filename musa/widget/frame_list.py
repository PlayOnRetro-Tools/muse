from PyQt5.QtCore import QAbstractListModel, QModelIndex, QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QSpinBox,
    QStyle,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
)

from musa.model.animation_collection import AnimationCollection


class FrameListModel(QAbstractListModel):
    def __init__(self, data_model: AnimationCollection, parent=None):
        super().__init__(parent)
        self.data_model = data_model
        self.current_animation = -1

    def rowCount(self, parent=QModelIndex()):
        if self.current_animation < 0:
            return 0
        return len(self.data_model.get_frames(self.current_animation))

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or self.current_animation < 0:
            return None

        frame = self.data_model.get_frames(self.current_animation)[index.row()]

        if role == Qt.DisplayRole:
            return frame.name
        elif role == Qt.UserRole:  # Use UserRole to store duration
            return frame.duration

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or self.current_animation < 0:
            return False

        if role == Qt.UserRole:  # For duration updates
            self.data_model.set_frame_duration(
                self.current_animation, index.row(), value
            )
            self.dataChanged.emit(index, index, [role])
            return True

        return False

    def set_current_animation(self, animation_index):
        self.beginResetModel()
        self.current_animation = animation_index
        self.endResetModel()


class FrameItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.duration_changed = pyqtSignal(QModelIndex, int)

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setRange(1, 1000)
        editor.setValue(index.data(Qt.UserRole))
        return editor

    def setEditorData(self, editor, index):
        editor.setValue(index.data(Qt.UserRole))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), Qt.UserRole)

    def sizeHint(self, option, index):
        return QSize(200, 40)

    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Draw the frame name
        painter.drawText(
            option.rect.adjusted(5, 5, -70, -5),
            Qt.AlignVCenter | Qt.AlignLeft,
            index.data(Qt.DisplayRole),
        )

        # Draw the duration value
        duration = str(index.data(Qt.UserRole))
        painter.drawText(
            option.rect.adjusted(option.rect.width() - 65, 5, -5, -5),
            Qt.AlignVCenter | Qt.AlignRight,
            f"{duration} Ticks",
        )


class FrameListWidget(QWidget):
    def __init__(self, model: AnimationCollection, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.data_model = model
        self.frame_model = FrameListModel(self.data_model)
        self.list.setModel(self.frame_model)
        self.list.setItemDelegate(FrameItemDelegate())

    def setup_ui(self):
        layout = QVBoxLayout()

        title_lay = QHBoxLayout()
        self.title = QLabel("Frames")
        title_lay.addWidget(self.title)

        list_lay = QVBoxLayout()
        self.list = QListView()
        list_lay.addWidget(self.list)

        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignTop)
        self.add_btn = QPushButton("+")
        self.del_btn = QPushButton("-")
        self.add_btn.setFixedSize(32, 32)
        self.del_btn.setFixedSize(32, 32)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.del_btn)

        hbox = QHBoxLayout()
        hbox.addLayout(list_lay)
        hbox.addLayout(btn_layout)

        layout.addLayout(title_lay)
        layout.addLayout(hbox)

        self.setLayout(layout)
