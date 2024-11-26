from typing import Any, List, Optional
from uuid import UUID

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

from musa.model.animation import Animation
from musa.model.frame import Frame


class FrameListModel(QAbstractListModel):
    def __init__(self, animation: Animation, parent=None):
        super().__init__(parent)
        self.animation = animation
        self.frames: List[UUID] = []

    def _refresh_frame_list(self):
        self.frames = [f.id for f in self.animation.frames]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.frames)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid() or not 0 <= index.row() < len(self.frames):
            return None

        frame = self.animation.get_frame(self.frames[index.row()])

        if role == Qt.DisplayRole:
            return frame.name
        elif role == Qt.EditRole:
            return frame.ticks
        elif role == Qt.UserRole:
            return frame.ticks

        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index) | Qt.ItemIsEditable

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or not 0 <= index.row() < len(self.animation.frames):
            return False

        if role == Qt.UserRole:
            frame = self.animation.get_frame(self.frames[index.row()])
            self.animation.update_frame(frame.id, ticks=value)
            self.animation.mark_frame_modified(frame.id)

            self.dataChanged.emit(index, index)
            return True

        return False

    def set_current_animation(self, animation: Animation):
        self.beginResetModel()
        self.animation = animation
        self._refresh_frame_list()

        # connect to animation signals
        self.animation.signals.frameAdded.connect(self._on_frame_changed)
        self.animation.signals.frameRemoved.connect(self._on_frame_changed)
        self.animation.signals.frameModified.connect(self._on_frame_modified)
        self.animation.signals.animationModified.connect(self._on_animation_modified)

        self.endResetModel()

    def _on_frame_changed(self, animation_id: UUID, frame_id: Optional[UUID] = None):
        if animation_id == self.animation.id:
            self.beginResetModel()
            self._refresh_frame_list()
            self.endResetModel()

    def _on_frame_modified(self, animation_id: UUID, frame_id: UUID):
        if animation_id == self.animation.id:
            try:
                row = next(
                    i
                    for i, frame in enumerate(self.animation.frames)
                    if frame.id == frame_id
                )
                index = self.index(row, 0)
                self.dataChanged.emit(index, index)
            except StopIteration:
                pass

    def _on_animation_modified(self, animation_id: UUID):
        if animation_id == self.animation.id:
            self.beginResetModel()
            self._refresh_frame_list()
            self.endResetModel()


class FrameItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index: QModelIndex):
        editor = QSpinBox(parent)
        editor.setRange(1, 1000)
        editor.setValue(index.data(Qt.UserRole))
        return editor

    def setEditorData(self, editor: QSpinBox, index: QModelIndex):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(value)

    def setModelData(
        self, editor: QSpinBox, model: QAbstractListModel, index: QModelIndex
    ):
        value = editor.value()
        model.setData(index, value, Qt.UserRole)

    def sizeHint(self, option, index):
        return QSize(90, 25)

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
        ticks = str(index.data(Qt.EditRole))
        painter.drawText(
            option.rect.adjusted(option.rect.width() - 65, 5, -5, -5),
            Qt.AlignVCenter | Qt.AlignRight,
            f"{ticks}",
        )


class FrameListWidget(QWidget):
    def __init__(self, animation: Animation = None, parent=None):
        super().__init__(parent)
        self.setup_ui()

        # Default buttons state
        self.add_btn.setEnabled(False)
        self.del_btn.setEnabled(False)

        self.animation = animation
        self.frame_model = FrameListModel(self.animation)
        self.list.setModel(self.frame_model)
        self.list.setItemDelegate(FrameItemDelegate())

        # connections
        self.add_btn.clicked.connect(self._on_frame_add)
        self.del_btn.clicked.connect(self._on_frame_remove)

    def set_animation(self, animation: Animation):
        self.animation = animation
        self.frame_model.set_current_animation(self.animation)
        self.add_btn.setEnabled(True)

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

    def _on_frame_add(self):
        base_name = self.animation.name
        index = len(self.animation.frames)
        dummy = Frame(name=f"{base_name.upper()} {index}")
        self.animation.add_frame(dummy)

    def _on_frame_remove(self):
        pass
