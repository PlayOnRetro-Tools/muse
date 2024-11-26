from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from musa.widget.animation_list import AnimationListWidget
from musa.widget.frame_list import FrameListWidget
from musa.widget.sprite_inspector import SpriteInspector
from musa.widget.sprite_list import SpriteListWidget


class AnimationDock(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setup_ui(model)
        self.connections()

    def setup_ui(self, model):
        layout = QHBoxLayout()

        self.animation_list = AnimationListWidget(model)
        self.frame_list = FrameListWidget(model)
        self.sprite_list = SpriteListWidget(model)
        self.sprite_inspector = SpriteInspector()

        layout.addWidget(self.animation_list, 1)
        layout.addWidget(self.frame_list, 1)
        layout.addWidget(self.sprite_list, 2)
        layout.addWidget(self.sprite_inspector, 2)

        self.setLayout(layout)

    def connections(self):
        self.animation_list.list.selectionModel().currentChanged.connect(
            self._on_animation_selected
        )
        self.frame_list.list.selectionModel().currentChanged.connect(
            self._on_frame_selected
        )
        self.sprite_list.spriteSelected.connect(self.sprite_inspector.update_sprite)

    def _on_animation_selected(self, current: QItemSelectionModel, previous):
        animation_index = current.row() if current.isValid() else -1
        self.frame_list.frame_model.set_current_animation(animation_index)
        # Clear sprites when animation changes
        self.sprite_list.sprite_model.set_current_frame(-1, -1)

    def _on_frame_selected(self, current: QItemSelectionModel, previous):
        if not current.isValid():
            self.sprite_list.sprite_model.set_current_frame(-1, -1)
            return
        animation_index = self.animation_list.list.currentIndex().row()
        frame_index = current.row()
        self.sprite_list.sprite_model.set_current_frame(animation_index, frame_index)

    def _on_property_changed(self, property_name, value):
        current = self.sprites_list.list.currentIndex()
        if not current.isValid():
            return

        animation_index = self.animations_list.list.currentIndex().row()
        frame_index = self.frames_list.list.currentIndex().row()
        sprite_index = current.row()

        self.data_model.set_sprite_property(
            animation_index, frame_index, sprite_index, property_name, value
        )
