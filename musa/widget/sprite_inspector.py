from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QHBoxLayout,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from musa.model.sprite import Sprite
from musa.widget.slider import ValueSlider


class SpriteInspector(QWidget):
    propertyChanged = pyqtSignal(str, object)  # property, value

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_sprite: Sprite = None

        self.setup_ui()
        self.set_sprite(None)
        self.connections()

    def connections(self):
        self.x_spin.valueChanged.connect(self._on_x_changed)
        self.y_spin.valueChanged.connect(self._on_y_changed)
        self.hflip.stateChanged.connect(self._on_hflip_changed)
        self.vflip.stateChanged.connect(self._on_vflip_changed)
        self.alpha_slider.valueChanged.connect(self._on_opacity_changed)

    def _on_x_changed(self, value: int):
        self.current_sprite.x = value

    def _on_y_changed(self, value: int):
        self.current_sprite.y = value

    def _on_hflip_changed(self, value: int):
        self.current_sprite.h_flip = value == Qt.Checked

    def _on_vflip_changed(self, value: int):
        self.current_sprite.v_flip = value == Qt.Checked

    def _on_opacity_changed(self, value: int):
        self.current_sprite.alpha = value

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.x_spin = QSpinBox()
        self.x_spin.setRange(-1024, 1024)
        self.x_spin.setValue(0)
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-1024, 1024)
        self.y_spin.setValue(0)
        self.hflip = QCheckBox("Horizontal")
        self.vflip = QCheckBox("Vertical")
        self.alpha_slider = ValueSlider(ValueSlider.Type.ALPHA)
        self.alpha_slider.setRange(0, 100)
        self.alpha_slider.setSingleStep(1)

        # Flip Container
        self.flip = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        hbox.addWidget(self.hflip)
        hbox.addWidget(self.vflip)
        self.flip.setLayout(hbox)

        form = QFormLayout()
        form.addRow("Alpha:", self.alpha_slider)
        form.addRow("X:", self.x_spin)
        form.addRow("Y:", self.y_spin)
        form.addRow("Flip:", self.flip)

        layout.addLayout(form)
        self.setLayout(layout)

    def set_sprite(self, sprite: Sprite):
        self.current_sprite = sprite

        if sprite is None:
            self.setEnabled(False)
            return

        self.setEnabled(True)

        # Block signals to prevent triggering updates
        self.x_spin.blockSignals(True)
        self.y_spin.blockSignals(True)
        self.hflip.blockSignals(True)
        self.vflip.blockSignals(True)
        self.alpha_slider.blockSignals(True)

        self.x_spin.setValue(sprite.x)
        self.y_spin.setValue(sprite.y)
        self.hflip.setChecked(sprite.h_flip)
        self.vflip.setChecked(sprite.v_flip)
        self.alpha_slider.setValue(sprite.alpha)

        self.x_spin.blockSignals(False)
        self.y_spin.blockSignals(False)
        self.hflip.blockSignals(False)
        self.vflip.blockSignals(False)
        self.alpha_slider.blockSignals(False)
