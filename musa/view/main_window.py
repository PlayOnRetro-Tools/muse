from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget

from musa.widget.event_filter import PanControl, ZoomControl
from musa.widget.palette import SpritePaletteWidget
from musa.widget.scene import EditorScene, EditorView


class MusaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("M.U.S.E")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)

        # Editor view
        self.scene = EditorScene()
        self.view = EditorView(self.scene)
        PanControl(self.view)
        ZoomControl(self.view)
        layout.addWidget(self.view, stretch=3)

        # Sprite palette
        self.palette = SpritePaletteWidget()
        palette_container = QWidget()
        palette_layout = QVBoxLayout(palette_container)
        palette_layout.addWidget(QLabel("Sprite Palette"))
        palette_layout.addWidget(self.palette)
        layout.addWidget(palette_container, stretch=1)

        self.setCentralWidget(central_widget)
