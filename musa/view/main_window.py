from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget

from musa.controller.animation_controller import AnimationController
from musa.manager import DockConfig, DockManager
from musa.model.animation import AnimationsModel
from musa.widget.event_filter import PanControl, ZoomControl
from musa.widget.palette import SpritePaletteWidget
from musa.widget.scene import EditorScene, EditorView

from .animation_dock import AnimationDock


class MusaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("M.U.S.E")

        # Model
        self.animation_model = AnimationsModel()

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

        animation = AnimationDock(self.animation_model, self)
        self.docks.create_dock(
            "ANIMATION",
            DockConfig(
                "Animation",
                Qt.BottomDockWidgetArea,
                Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea,
                animation,
            ),
        )

        self.setCentralWidget(content)
