from typing import List

from PyQt5.QtWidgets import QUndoCommand, QUndoStack

from .keyframe import KeyFrame, Track


class TimelineModel:
    def __init__(self):
        self.tracks: List[Track] = []
        self.start_frame = 0
        self.end_frame = 200
        self.current_frame = 0
        self.undo_stack = QUndoStack()

    def add_track(self, track: Track):
        self.tracks.append(track)

    def add_keyframe(self, track_index: int, frame: int, value: float):
        command = AddKeyFrameCommand(self, track_index, frame, value)
        self.undo_stack.push(command)

    def remove_keyframe(self, track_index: int, keyframe: KeyFrame):
        command = RemoveKeyFrameCommand(self, track_index, keyframe)
        self.undo_stack.push(command)

    def move_keyframe(
        self, track_index: int, keyframe: KeyFrame, new_frame: int, new_value: float
    ):
        command = MoveKeyFrameCommand(self, track_index, keyframe, new_frame, new_value)
        self.undo_stack.push(command)


class AddKeyFrameCommand(QUndoCommand):
    def __init__(
        self, model: TimelineModel, track_index: int, frame: int, value: float
    ):
        super().__init__("Add keyframe")
        self.model = model
        self.track_index = track_index
        self.keyframe = KeyFrame(frame, value)

    def redo(self):
        if 0 <= self.track_index < len(self.model.tracks):
            self.model.tracks[self.track_index].keyframes.append(self.keyframe)

    def undo(self):
        if 0 <= self.track_index < len(self.model.tracks):
            self.model.tracks[self.track_index].keyframes.remove(self.keyframe)


class RemoveKeyFrameCommand(QUndoCommand):
    def __init__(self, model: TimelineModel, track_index: int, keyframe: KeyFrame):
        super().__init__("Remove keyframe")
        self.model = model
        self.track_index = track_index
        self.keyframe = keyframe

    def redo(self):
        if 0 <= self.track_index < len(self.model.tracks):
            self.model.tracks[self.track_index].keyframes.remove(self.keyframe)

    def undo(self):
        if 0 <= self.track_index < len(self.model.tracks):
            self.model.tracks[self.track_index].keyframes.append(self.keyframe)


class MoveKeyFrameCommand(QUndoCommand):
    def __init__(
        self,
        model: TimelineModel,
        track_index: int,
        keyframe: KeyFrame,
        new_frame: int,
        new_value: float,
    ):
        super().__init__("Move keyframe")
        self.model = model
        self.track_index = track_index

        self.index = self.model.tracks[self.track_index].keyframes.index(keyframe)

        self.old_frame = keyframe.frame
        self.old_value = keyframe.value
        self.new_frame = new_frame
        self.new_value = new_value

    def redo(self):
        self.model.tracks[self.track_index].keyframes[self.index] = KeyFrame(
            self.new_frame, self.new_value
        )

    def undo(self):
        self.model.tracks[self.track_index].keyframes[self.index] = KeyFrame(
            self.old_frame, self.old_value
        )
