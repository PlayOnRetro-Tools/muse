from dataclasses import dataclass
from typing import List, Optional, Set

from PyQt5.QtGui import QColor


@dataclass
class KeyFrame:
    frame: int
    value: float


class Track:
    def __init__(self, name: str):
        self.name = name
        self.keyframes: List[KeyFrame] = []
        self.color = QColor(200, 200, 200)

    def get_keyframe_at_frame(self, frame: int) -> Optional[KeyFrame]:
        return next((kf for kf in self.keyframes if kf.frame == frame), None)

    def get_adjacent_keyframes(
        self, frame: int, exclude_frames: Set[int] = None
    ) -> tuple[Optional[KeyFrame], Optional[KeyFrame]]:
        """Get the nearest keyframes before and after the given frame, exlcuding specified frames."""
        if exclude_frames is None:
            exclude_frames = set()

        prev_kf = None
        next_kf = None

        sorted_keyframes = sorted(
            (kf for kf in self.keyframes if kf.frame not in exclude_frames),
            key=lambda x: x.frame,
        )

        for kf in sorted_keyframes:
            if kf.frame < frame:
                prev_kf = kf
            elif kf.frame > frame:
                next_kf = kf
                break

        return prev_kf, next_kf
