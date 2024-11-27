from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QWidget

from musa.model.frame import Frame
from musa.widget.sprite_inspector import SpriteInspector
from musa.widget.sprite_list import SpriteListWidget


class InspectorDock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connections()

    def connections(self):
        self.sprite_list.spriteSelected.connect(self.inspector.set_sprite)

    def set_frame(self, frame: Frame):
        self.sprite_list.set_frame(frame)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.sprite_list = SpriteListWidget()
        self.inspector = SpriteInspector()

        group_box = QGroupBox("Properties")
        group_box_lay = QVBoxLayout()
        group_box_lay.addWidget(self.inspector)
        group_box.setLayout(group_box_lay)

        layout.addWidget(self.sprite_list)
        layout.addWidget(group_box)

        self.setLayout(layout)
