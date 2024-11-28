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

        # Managers
        self.dock_manager = DockManager(self)

        # Main document model
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
        self.editor = EditorWidget()
        self.setCentralWidget(self.editor)
        self.palette = SpritePaletteWidget()
        self.animation = AnimationDock(self.animation_collection, self)
        self.inspector = InspectorDock()

        self.dock_manager.create_dock(
            "PALETTE",
            DockConfig(
                "Sprite Palette",
                DockConfig.Area.RIGHT,
                DockConfig.Area.LEFT | DockConfig.Area.RIGHT,
                self.palette,
            ),
        )

        self.dock_manager.create_dock(
            "ANIMATION",
            DockConfig(
                "Animation",
                DockConfig.Area.BOTTOM,
                DockConfig.Area.BOTTOM | DockConfig.Area.TOP,
                self.animation,
            ),
        )

        self.dock_manager.create_dock(
            "INSPECTOR",
            DockConfig(
                "Inspector",
                DockConfig.Area.RIGHT,
                DockConfig.Area.LEFT | DockConfig.Area.RIGHT,
                self.inspector,
            ),
        )
