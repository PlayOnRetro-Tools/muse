from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsRectItem

from musa.model.keyframe import KeyFrame, Track
from musa.model.timeline import TimelineModel


class KeyFrameItem(QGraphicsRectItem):
    _SIZE = 10

    def __init__(
        self, frame: int, value: float, track_index: int, model: TimelineModel
    ):
        super().__init__(-self._SIZE / 2, -self._SIZE / 2, self._SIZE, self._SIZE)

        self.frame = frame
        self.value = value
        self.track_index = track_index
        self.model = model

        self.original_pos = None
        self.original_frame = None
        self.original_value = None
        self.drag_start_pos = None

        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setBrush(QBrush(Qt.white))
        self.setPen(QPen(Qt.black))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.original_pos = self.pos()
            self.original_frame = self.frame
            self.original_value = self.value
            self.drag_start_pos = event.scenePos()

            # Store the original y position for maintining vertical position
            self.original_y = self.pos().y()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.original_pos is not None:
            # Calculate the new position
            new_pos = self.mapToScene(event.pos())

            # Restrict movement to x-axis
            new_pos.setY(self.original_y)

            # Convert position to frame number
            pixels_per_frame = self.scene().views()[0].pixels_per_frame
            new_frame = round(new_pos.x() / pixels_per_frame)

            # Get adjacent keyframes and check overlap
            track = self.model.tracks[self.track_index]
            prev_kf, next_kf = track.get_adjacent_keyframes(self.original_frame)

            # Prevent overlap with adjacent keyframes
            if prev_kf and new_frame <= prev_kf.frame:
                new_frame = prev_kf.frame + 1
            if next_kf and new_frame >= next_kf.frame:
                new_frame = next_kf.frame - 1

            # Enforce timeline boundaries
            new_frame = max(
                self.model.start_frame, min(new_frame, self.model.end_frame)
            )

            # Update position
            new_x = (new_frame * pixels_per_frame) + self.scene().views()[
                0
            ]._LEFT_OFFSET
            self.setPos(new_x, self.original_y)

    def mouseReleaseEvent(self, event):
        new_frame = None
        new_value = None

        if event.button() == Qt.LeftButton and self.original_pos != self.pos():
            new_frame = round(
                (self.pos().x() - self.scene().views()[0]._LEFT_OFFSET)
                / self.scene().views()[0].pixels_per_frame
            )

            # Compute!!
            new_value = self.value

            # Reset tracking variables
            self.original_pos = None
            self.drag_start_pos = None

        super().mouseReleaseEvent(event)

        # Only create undo command in the position actually changed
        if new_frame != self.original_frame:
            keyframe = KeyFrame(self.original_frame, self.original_value)
            self.model.move_keyframe(self.track_index, keyframe, new_frame, new_value)


class TrackItem(QGraphicsRectItem):
    _HEIGHT = 30

    def __init__(self, track: Track, width: int):
        super().__init__(0, 0, width, self._HEIGHT)
        self.setPen(QPen(track.color))
        self.setBrush(QBrush(track.color.lighter(150)))
