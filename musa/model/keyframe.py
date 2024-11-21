from dataclasses import dataclass
from typing import List, Optional

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
        self, frame: int
    ) -> tuple[Optional[KeyFrame], Optional[KeyFrame]]:
        """Get the nearest keyframes before and after the given frame."""
        prev_kf = None
        next_kf = None

        for kf in sorted(self.keyframes, key=lambda x: x.frame):
            if kf.frame < frame:
                prev_kf = kf
            elif kf.frame > frame:
                next_kf = kf
                break

        return prev_kf, next_kf
