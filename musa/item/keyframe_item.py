from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QAction, QGraphicsRectItem, QMenu

from musa.model.keyframe import KeyFrame, Track
from musa.model.timeline import (
    MacroCommand,
    MergeKeyFramesCommand,
    MoveKeyFrameCommand,
    TimelineModel,
)


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

    def paint(self, painter, option, widget):
        if self.isSelected():
            self.setBrush(QBrush(Qt.yellow))
        else:
            self.setBrush(QBrush(Qt.white))
        super().paint(painter, option, widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.original_pos = self.pos()
            self.original_frame = self.frame
            self.original_value = self.value
            self.drag_start_pos = event.scenePos()
            self.original_y = self.pos().y()

            # Handle multi-selection with Ctrl/Shift
            if not (event.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)):
                # Clear selection
                for item in self.scene().selectedItems():
                    if item != self:
                        item.setSelected(False)

        elif event.button() == Qt.RightButton:
            self.showContextMenu(event)

        super().mousePressEvent(event)

    def showContextMenu(self, event):
        menu = QMenu()
        selected_items = self.scene().selectedItems()

        if len(selected_items) > 1:
            merge_action = QAction("Merge keyframes", menu)
            merge_action.triggered.connect(
                lambda: self.merge_selected_keyframes(selected_items)
            )
            menu.addAction(merge_action)

        if menu.actions():
            menu.exec_(event.screenPos())

    def merge_selected_keyframes(self, selected_items: "KeyFrameItem"):
        # Only merge items from the same track
        items_by_track = {}
        for item in selected_items:
            if item.track_index not in items_by_track:
                items_by_track[item.track_index] = []
            items_by_track[item.track_index].append(item)

        # Merge keyframes in eack track
        for track_index, items in items_by_track.items():
            if len(items) > 1:
                # Use the average frame as the target
                frames = [item.frame for item in items]
                target_frame = round(sum(frames) / len(frames))

                # Create and execute merge command
                command = MergeKeyFramesCommand(
                    self.model, track_index, frames, target_frame
                )
                self.model.undo_stack.push(command)

        # Rebuild the scene
        self.scene().parent().setup_timeline()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.original_pos is not None:
            # Get all selected items
            selected_items = self.scene().selectedItems()
            if not selected_items:
                selected_items = [self]

            # Calculate the movement delta in frames
            new_pos = self.mapToScene(event.pos())
            pixels_per_frame = self.scene().views()[0].pixels_per_frame
            delta_frames = round(
                (new_pos.x() - self.original_pos.x()) / pixels_per_frame
            )

            # Check if movement is valid for all selected items
            can_move = True
            for item in selected_items:
                new_frame = item.original_frame + delta_frames
                track = self.model.tracks[item.track_index]

                # Get adjacent keyframes, excluding other selected keyframes
                selected_frames = {i.frame for i in selected_items}
                prev_kf, next_kf = track.get_adjacent_keyframes(
                    item.original_frame, exclude_frames=selected_frames
                )

                # Check boundaries
                if (
                    (prev_kf and new_frame <= prev_kf.frame)
                    or (next_kf and new_frame >= next_kf.frame)
                    or new_frame < self.model.start_frame
                    or new_frame > self.model.end_frame
                ):
                    can_move = False
                    break

            # Move all selected items if valid
            if can_move:
                for item in selected_items:
                    new_x = (item.original_frame + delta_frames) * pixels_per_frame
                    item.setPos(new_x, item.original_y)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.original_pos != self.pos():
            # Handle group movement
            selected_items = self.scene().selectedItems()
            if selected_items:
                # Create compound undo command for all moved items
                commands = []
                for item in selected_items:
                    new_frame = round(
                        (item.pos().x() - self.scene().views()[0]._LEFT_OFFSET)
                        / self.scene().views()[0].pixels_per_frame
                    )
                    if new_frame != item.original_frame:
                        commands.append(
                            MoveKeyFrameCommand(
                                self.model,
                                item.track_index,
                                KeyFrame(item.original_frame, item.value),
                                new_frame,
                                item.value,
                            )
                        )

                if len(commands) > 0:
                    self.model.undo_stack.push(
                        MacroCommand("Move multiple keyframes", commands)
                    )

        self.original_pos = None
        self.drag_start_pos = None
        super().mouseReleaseEvent(event)


class TrackItem(QGraphicsRectItem):
    _HEIGHT = 30

    def __init__(self, track: Track, width: int):
        super().__init__(0, 0, width, self._HEIGHT)
        self.setPen(QPen(track.color))
        self.setBrush(QBrush(track.color.lighter(150)))
