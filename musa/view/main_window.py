from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from musa.manager import DockConfig, DockManager
from musa.model.animation_collection import AnimationCollection
from musa.widget.palette import SpritePaletteWidget

from .animation_dock import AnimationDock
from .editor_widget import EditorWidget
from .inspector_dock import InspectorDock


class MusaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("M.U.S.E")

        # Model
        self.animation_collection = AnimationCollection()

        self.setup_ui()
        self.connections()

    def connections(self):
        self.animation.frameSelected.connect(self.inspector.set_frame)
        self.animation.frameSelected.connect(self.editor.set_frame)
        self.animation.animationSelected.connect(self.editor.set_animation)

        # Enable editing when a new animation is created
        self.animation_collection.signals.animationAdded.connect(
            lambda x: self.editor.setEnabled(True)
        )

    def setup_ui(self):
        self.docks = DockManager(self)

        self.editor = EditorWidget()

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

        self.animation = AnimationDock(self.animation_collection, self)
        self.docks.create_dock(
            "ANIMATION",
            DockConfig(
                "Animation",
                Qt.BottomDockWidgetArea,
                Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea,
                self.animation,
            ),
        )

        self.inspector = InspectorDock()
        self.docks.create_dock(
            "INSPECTOR",
            DockConfig(
                "Inspector",
                Qt.RightDockWidgetArea,
                Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea,
                self.inspector,
            ),
        )

        self.setCentralWidget(self.editor)
