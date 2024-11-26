from uuid import UUID

from PyQt5.QtCore import QObject, pyqtSignal


class AnimationSignals(QObject):
    frameAdded = pyqtSignal(UUID)  # animation id
