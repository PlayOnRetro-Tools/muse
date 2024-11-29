from typing import Dict

from PyQt5.QtCore import QFile, QIODevice, Qt
from PyQt5.QtGui import QIcon, QPixmap

import musa.resources.resources


class ResourceManager:
    _icon_cache: Dict[str, QIcon] = {}
    _pixmap_cache: Dict[str, QPixmap] = {}

    @staticmethod
    def get_icon(name: str) -> QIcon:
        if name not in ResourceManager._icon_cache:
            ResourceManager._icon_cache[name] = QIcon(f":icons/{name}")
        return ResourceManager._icon_cache[name]

    @staticmethod
    def get_scaled_icon(name: str, size: int) -> QIcon:
        id = f"{name}_{size}"
        if id not in ResourceManager._icon_cache:
            pixmap = QPixmap(f":icons/{name}").scaled(
                size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            ResourceManager._icon_cache[id] = QIcon(pixmap)
        return ResourceManager._icon_cache[id]

    @staticmethod
    def get_pixmap(name: str) -> QPixmap:
        if name not in ResourceManager._pixmap_cache:
            ResourceManager._pixmap_cache[name] = QPixmap(f":image/{name}")
        return ResourceManager._pixmap_cache[name]

    @staticmethod
    def get_scaled_pixmap(name: str, size: int) -> QPixmap:
        id = f"{name}_{size}"
        if id not in ResourceManager._pixmap_cache:
            pixmap = QPixmap(f":image/{name}").scaled(
                size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            ResourceManager._pixmap_cache[id] = pixmap
        return ResourceManager._pixmap_cache[id]

    @staticmethod
    def get_stylesheet(name: str) -> str:
        file = QFile(f":styles/{name}")
        if file.open(QIODevice.ReadOnly | QIODevice.Text):
            return str(file.readAll(), encoding="utf-8")
        return ""
