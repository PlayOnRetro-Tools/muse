from PyQt5.QtWidgets import QVBoxLayout, QWidget

from musa.model.animation import Animation
from musa.model.frame import Frame
from musa.widget.editor import EditorScene, EditorView
from musa.widget.event_filter import PanControl, ZoomControl


class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEnabled(False)

        self.scene = EditorScene()
        self.view = EditorView(self.scene)
        PanControl(self.view)
        ZoomControl(self.view)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def set_frame(self, frame: Frame):
        self.scene.set_frame(frame)

    def set_animation(self, animation: Animation):
        self.scene.set_animation(animation)
