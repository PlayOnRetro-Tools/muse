from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget

from musa.manager import DockConfig, DockManager
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
        content = QWidget()
        layout = QHBoxLayout(content)

        self.docks = DockManager(self)

        # Editor view
        self.scene = EditorScene()
        self.view = EditorView(self.scene)
        PanControl(self.view)
        ZoomControl(self.view)
        layout.addWidget(self.view)

        # Sprite palette
        palette = SpritePaletteWidget()
        self.docks.create_dock(
            "PALETTE",
            DockConfig(
                "Sprite Palette",
                Qt.RightDockWidgetArea,
                Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea,
                palette,
            ),
        )

        self.setCentralWidget(content)
