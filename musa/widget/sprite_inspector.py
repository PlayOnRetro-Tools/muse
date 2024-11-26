from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from musa.model.piece import Piece


class SpriteInspector(QWidget):
    propertyChanged = pyqtSignal(str, object)  # property, value

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_sprite: Piece = None

        self.setup_ui()
        self.update_sprite(None)

        # Connections
        self.x_pos_spin.valueChanged.connect(
            lambda value: self.propertyChanged.emit("x", value)
        )
        self.y_pos_spin.valueChanged.connect(
            lambda value: self.propertyChanged.emit("y", value)
        )
        self.hflip_check_box.stateChanged.connect(
            lambda state: self.propertyChanged.emit("flip_h", state == Qt.Checked)
        )
        self.vflip_check_box.stateChanged.connect(
            lambda state: self.propertyChanged.emit("flip_v", state == Qt.Checked)
        )

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.name = QLabel("Inspector")
        layout.addWidget(self.name)

        self.x_pos_spin = QSpinBox()
        self.x_pos_spin.setValue(0)
        self.y_pos_spin = QSpinBox()
        self.y_pos_spin.setValue(0)
        self.hflip_check_box = QCheckBox("Horizontal")
        self.vflip_check_box = QCheckBox("Vertical")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setSingleStep(1)

        # Flip Container
        self.flip = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        hbox.addWidget(self.hflip_check_box)
        hbox.addWidget(self.vflip_check_box)
        self.flip.setLayout(hbox)

        form = QFormLayout()
        form.addRow("X:", self.x_pos_spin)
        form.addRow("Y:", self.y_pos_spin)
        form.addRow("Opacity:", self.opacity_slider)
        form.addRow("Flip:", self.flip)
        container = QFrame()
        container.setFrameStyle(QFrame.StyledPanel)
        container.setLayout(form)

        layout.addWidget(container)
        self.setLayout(layout)

    def update_sprite(self, sprite: Piece):
        self.current_sprite = sprite
        if sprite is None:
            self.setEnabled(False)
            return

        self.setEnabled(True)

        # Block signals to prevent triggering updates
        self.x_pos_spin.blockSignals(True)
        self.y_pos_spin.blockSignals(True)
        self.hflip_check_box.blockSignals(True)
        self.vflip_check_box.blockSignals(True)

        self.x_pos_spin.setValue(sprite.x)
        self.y_pos_spin.setValue(sprite.y)
        self.hflip_check_box.setChecked(sprite.h_flip)
        self.vflip_check_box.setChecked(sprite.v_flip)

        self.x_pos_spin.blockSignals(False)
        self.y_pos_spin.blockSignals(False)
        self.hflip_check_box.blockSignals(False)
        self.vflip_check_box.blockSignals(False)
