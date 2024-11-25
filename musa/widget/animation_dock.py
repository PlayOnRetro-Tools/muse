from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from musa.controller.animation_controller import AnimationController
from musa.model.animation import AnimationsModel

from .piece_inspector import PieceInspector
from .playback_control import PlayBackWidget


class FrameListItem(QWidget):
    def __init__(self, name: str, ticks: int = 1):
        super().__init__()
        self.setup_ui(name, ticks)

    def setup_ui(self, name: str, ticks: int):
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 0, 2)

        self.name = QLabel(name)
        self.ticks_spin = QSpinBox()
        self.ticks_spin.setMinimum(1)
        self.ticks_spin.setValue(ticks)

        layout.addWidget(self.name)
        layout.addStretch()
        layout.addWidget(self.ticks_spin)
        self.setLayout(layout)


class ListWidget(QWidget):
    itemSelected = pyqtSignal(QListWidgetItem)
    itemEditChanged = pyqtSignal(QListWidgetItem)
    addClicked = pyqtSignal(int)
    delClicked = pyqtSignal(int)
    upClicked = pyqtSignal()
    downClicked = pyqtSignal()

    def __init__(
        self, title: str, order_btn: bool = False, allow_edit: bool = True, parent=None
    ):
        super().__init__(parent)
        self.allow_edit = allow_edit

        self.setup_ui(title, order_btn)

        self.list.setEditTriggers(
            QListWidget.DoubleClicked | QListWidget.EditKeyPressed
        )
        self.list.itemClicked.connect(self.itemSelected)
        self.list.itemChanged.connect(self.itemEditChanged)

        # Connections
        if not order_btn:
            self.add_btn.clicked.connect(
                lambda x: self.addClicked.emit(self.list.currentRow())
            )
            self.del_btn.clicked.connect(
                lambda x: self.delClicked.emit(self.list.currentRow())
            )

    def add_item(self, text: str, ticks: int = None):
        if ticks:
            item = QListWidgetItem(self.list)
            frame_item = FrameListItem(text, ticks)
            item.setSizeHint(frame_item.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, frame_item)
        else:
            item = QListWidgetItem(text)
            self.list.addItem(item)

        if self.allow_edit:
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    def clear(self):
        self.list.clear()

    def setup_ui(self, title: str, order_btn: bool):
        layout = QVBoxLayout()

        self.title = QLabel(title)
        self.list = QListWidget()
        layout.addWidget(self.title)
        layout.addWidget(self.list)

        hbox = QHBoxLayout()
        hbox.addStretch()

        if order_btn:
            self.up_btn = QPushButton("^")
            self.down_btn = QPushButton("<")
            self.up_btn.setFixedWidth(32)
            self.down_btn.setFixedWidth(32)
            hbox.addWidget(self.up_btn)
            hbox.addWidget(self.down_btn)

        else:
            self.add_btn = QPushButton("+")
            self.del_btn = QPushButton("-")
            self.add_btn.setFixedWidth(32)
            self.del_btn.setFixedWidth(32)
            hbox.addWidget(self.add_btn)
            hbox.addWidget(self.del_btn)

        layout.addLayout(hbox)
        self.setLayout(layout)


class AnimationDock(QWidget):
    def __init__(
        self, model: AnimationsModel, controller: AnimationController, parent=None
    ):
        super().__init__(parent)
        self.controller = controller
        self.model = model

        self.setup_ui()
        self.make_connections()
        self.populate()

    def populate(self):
        for animation in self.model.get_animations():
            self.animation_list.add_item(animation)

    def make_connections(self):
        self.animation_list.addClicked.connect(self.controller.add_animation)
        self.animation_list.itemSelected.connect(self._on_animation_selected)

        self.frame_list.addClicked.connect(self.controller.add_frame)
        self.frame_list.itemSelected.connect(self._on_frame_selected)

        self.piece_list.itemSelected.connect(self._on_piece_selected)

        self.model.createdAnimation.connect(self._on_add_animation)

    def _on_animation_selected(self, item: QListWidgetItem):
        animation = self.model.get_animation(item.text())

        self.frame_list.clear()
        self.piece_list.clear()

        for frame in animation:
            self.frame_list.add_item(frame.name, frame.ticks)

    def _on_frame_selected(self, item: QListWidget):
        anim_name = self.animation_list.list.currentItem().text()
        animation = self.model.get_animation(anim_name)
        frame = animation.get_frame(self.frame_list.list.row(item))

        self.piece_list.clear()
        for piece in frame:
            self.piece_list.add_item(piece.name)

    def _on_piece_selected(self, item: QListWidgetItem):
        anim_name = self.animation_list.list.currentItem().text()
        animation = self.model.get_animation(anim_name)
        frame = animation.get_frame(self.frame_list.list.currentRow())

        piece = frame.get_piece(item.text())
        self.piece_inspector.show_piece(piece)

    def _on_add_animation(self, name: str):
        self.animation_list.add_item(name)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.playback = PlayBackWidget(self)
        layout.addWidget(self.playback)
        self.playback.hide()

        hbox_layout = QHBoxLayout()
        self.animation_list = ListWidget("Animations")
        self.frame_list = ListWidget("Frames", allow_edit=False)
        self.piece_list = ListWidget("Pieces", True, False)
        self.piece_inspector = PieceInspector()
        hbox_layout.addWidget(self.animation_list)
        hbox_layout.addWidget(self.frame_list)
        hbox_layout.addWidget(self.piece_list)
        hbox_layout.addWidget(self.piece_inspector, 2)
        hbox_layout.setAlignment(Qt.AlignJustify)
        layout.addLayout(hbox_layout)

        self.setLayout(layout)
