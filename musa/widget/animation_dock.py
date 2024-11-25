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
    currentSelectedChanged = pyqtSignal(QListWidgetItem, QListWidgetItem)
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
        self.list.currentItemChanged.connect(self.currentSelectedChanged)
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
        self.setup_ui()

        self.controller = controller
        self.model = model

        # Make connections
        self.animation_list.addClicked.connect(self.controller.add_animation)
        self.frame_list.addClicked.connect(self.controller.add_frame)

    def setup_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout()

        control_layout = QHBoxLayout()

        self.play_btn = QPushButton("Play")
        self.stop_btn = QPushButton("Stop")
        self.prev_btn = QPushButton("<")
        self.next_btn = QPushButton(">")

        self.play_btn.setCheckable(True)

        self.fps_label = QLabel("Fps:")
        self.fps_spin = QSpinBox()
        self.fps_spin.setMaximum(60)
        self.fps_spin.setMinimum(1)
        self.fps_spin.setValue(16)

        control_layout.addStretch()
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.next_btn)
        control_layout.addWidget(self.fps_label)
        control_layout.addWidget(self.fps_spin)
        control_layout.addStretch()
        control_layout.setAlignment(Qt.AlignLeft)
        layout.addLayout(control_layout)

        hbox_layout = QHBoxLayout()
        self.animation_list = ListWidget("Animations")
        self.frame_list = ListWidget("Frames", allow_edit=False)
        self.piece_list = ListWidget("Pieces", True, False)
        self.piece_inspector = PieceInspector()
        hbox_layout.addWidget(self.animation_list, 1)
        hbox_layout.addWidget(self.frame_list, 2)
        hbox_layout.addWidget(self.piece_list, 1)
        hbox_layout.addWidget(self.piece_inspector, 2)
        layout.addLayout(hbox_layout)

        self.setLayout(layout)
