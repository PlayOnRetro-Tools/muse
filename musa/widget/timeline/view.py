import math

from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

from musa.item.keyframe_item import KeyFrameItem, TrackItem
from musa.model.keyframe import KeyFrame, Track
from musa.model.timeline import TimelineModel


class TimelineView(QGraphicsView):
    frameSelected = pyqtSignal(int)

    _PIXELS_PER_FRAME = 10
    _LEFT_OFFSET = 20

    def __init__(self, model: TimelineModel):
        super().__init__()
        self.model = model
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)

        # Visual settings
        self.pixels_per_frame = self._PIXELS_PER_FRAME
        self.timeline_height = 0

        self.model.modelChanged.connect(self.setup_timeline)

        self.setup_timeline()

    def setup_timeline(self):
        self.scene.clear()

        # Calculate dimensions
        width = (
            (self.model.end_frame - self.model.start_frame) * self.pixels_per_frame
        ) - self._LEFT_OFFSET

        # Time ruler
        self.draw_ruler(width)

        # Draw tracks
        for track_index, track in enumerate(self.model.tracks):
            y_pos = (track_index + 1) * TrackItem._HEIGHT
            item = TrackItem(track, width)
            item.setPos(self._LEFT_OFFSET, y_pos)
            self.scene.addItem(item)

            # Draw keyframes
            for keyframe in sorted(track.keyframes, key=lambda x: x.frame):
                x = (keyframe.frame * self.pixels_per_frame) + self._LEFT_OFFSET
                y = y_pos + TrackItem._HEIGHT / 2
                key_item = KeyFrameItem(
                    keyframe.frame, keyframe.value, track_index, self.model
                )
                key_item.setPos(x, y)
                self.scene.addItem(key_item)

        # Update scene rect
        self.timeline_height = (len(self.model.tracks) + 1) * TrackItem._HEIGHT
        self.scene.setSceneRect(QRectF(0, 0, width, self.timeline_height))

    def draw_ruler(self, width: int):
        ruler_height = 20

        # Draw main line
        self.scene.addLine(self._LEFT_OFFSET, 0, width, 0, QPen(Qt.black))

        # Draw ticks and labels
        for frame in range(self.model.start_frame, self.model.end_frame + 1, 5):
            x = (frame * self.pixels_per_frame) + self._LEFT_OFFSET
            # Major tick every 5 frames
            tick_height = ruler_height / 2 if frame % 10 == 0 else ruler_height / 4
            self.scene.addLine(x, 0, x, tick_height, QPen(Qt.black))

            if frame % 10 == 0:
                text = self.scene.addText(str(frame))
                text.setPos(x - text.boundingRect().width() / 2, tick_height)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            # Zoom
            zoom_factor = 1.1 if event.angleDelta().y() > 0 else 0.9
            self.pixels_per_frame *= zoom_factor
            self.setup_timeline()
        else:
            # Normal scroll
            super().wheelEvent(event)
