from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QToolBar, QWidget

from musa.manager import DockConfig, DockManager
from musa.model.keyframe import KeyFrame, Track
from musa.widget.event_filter import PanControl, ZoomControl
from musa.widget.palette import SpritePaletteWidget
from musa.widget.scene import EditorScene, EditorView
from musa.widget.timeline import TimelineModel, TimelineView


class MusaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("M.U.S.E")

        # Models
        self.timeline_model = TimelineModel()

        # Test data
        track1 = Track("Position")
        track1.keyframes = [KeyFrame(30, 105), KeyFrame(80, 10)]

        track2 = Track("Scale")
        track2.keyframes = [KeyFrame(30, 105), KeyFrame(80, 10)]

        track3 = Track("Rotation")
        track3.keyframes = [KeyFrame(50, 105), KeyFrame(100, 10)]

        self.timeline_model.add_track(track1)
        self.timeline_model.add_track(track2)
        self.timeline_model.add_track(track3)

        self.setup_ui()
        self.create_toolbar()

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

        # Animation timeline
        timeline = TimelineView(self.timeline_model)
        self.docks.create_dock(
            "TIMELINE",
            DockConfig(
                "Animation",
                Qt.BottomDockWidgetArea,
                Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea,
                timeline,
            ),
        )

        self.setCentralWidget(content)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        undo = self.timeline_model.undo_stack.createUndoAction(self, "Undo")
        undo.setShortcut("Ctrl+Z")
        redo = self.timeline_model.undo_stack.createRedoAction(self, "Redo")
        redo.setShortcut("Ctrl+R")

        toolbar.addAction(undo)
        toolbar.addAction(redo)
