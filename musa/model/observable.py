from uuid import UUID

from PyQt5.QtCore import QObject, pyqtSignal


class AnimationSignals(QObject):
    frameAdded = pyqtSignal(UUID)  # animation id
    frameRemoved = pyqtSignal(UUID, UUID)  # animation id, frame id
    frameModified = pyqtSignal(UUID, UUID)  # animation id, frame id
    animationModified = pyqtSignal(UUID)  # animation id


class CollectionSignals(QObject):
    animationAdded = pyqtSignal(UUID)  # animation id
    animationRemoved = pyqtSignal(UUID)  # animation id
    animationModified = pyqtSignal(UUID)  # animation id
    collectionLoaded = pyqtSignal()  # entire collection has been loaded
