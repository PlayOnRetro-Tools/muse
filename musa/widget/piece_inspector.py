from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QFrame,
    QLabel,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from musa.model.piece import Piece


class PieceInspector(QWidget):
    pieceEdited = pyqtSignal(Piece)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_piece: Piece = None

        self.setup_ui()
        self.show_piece(None)

        # Connections
        self.x_pos_spin.valueChanged.connect(self._on_x_pos_changed)
        self.y_pos_spin.valueChanged.connect(self._on_y_pos_changed)
        self.hflip_check_box.clicked.connect(self._on_hflip_changed)
        self.vflip_check_box.clicked.connect(self._on_vflip_changed)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.name = QLabel("Inspector")
        layout.addWidget(self.name)

        self.x_pos_spin = QSpinBox()
        self.x_pos_spin.setValue(0)
        self.y_pos_spin = QSpinBox()
        self.y_pos_spin.setValue(0)
        self.hflip_check_box = QCheckBox()
        self.vflip_check_box = QCheckBox()

        form = QFormLayout()
        form.addRow("X:", self.x_pos_spin)
        form.addRow("Y:", self.y_pos_spin)
        form.addRow("Hflip:", self.hflip_check_box)
        form.addRow("Vflip:", self.vflip_check_box)
        container = QFrame()
        container.setFrameStyle(QFrame.StyledPanel)
        container.setLayout(form)

        layout.addWidget(container)
        self.setLayout(layout)

    def show_piece(self, piece: Piece):
        self.current_piece = piece
        if piece:
            self.x_pos_spin.setValue(piece.x)
            self.y_pos_spin.setValue(piece.y)
            self.hflip_check_box.setChecked(piece.h_flip)
            self.vflip_check_box.setChecked(piece.v_flip)
            self.setEnabled(True)
        else:
            self.setEnabled(False)

    def _on_x_pos_changed(self, value: int):
        self.current_piece.x = value
        self.pieceEdited.emit(self.current_piece)

    def _on_y_pos_changed(self, value: int):
        self.current_piece.y = value
        self.pieceEdited.emit(self.current_piece)

    def _on_hflip_changed(self, value: bool):
        self.current_piece.h_flip = value
        self.pieceEdited(self.current_piece)

    def _on_vflip_changed(self, value: bool):
        self.current_piece.v_flip = value
        self.pieceEdited(self.current_piece)
