from pathlib import Path


class SpriteSheet:
    def __init__(self, path: Path, base_name: str, frame_width: int, frame_height: int):
        self.path = path
        self.base_name = base_name
        self.frame_width = frame_width
        self.frame_height = frame_height
