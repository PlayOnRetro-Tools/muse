from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)


class TextInputDialog(QDialog):
    def __init__(
        self,
        title: str = "Input",
        label: str = "Enter Name:",
        default: str = "",
        parent=None,
    ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setModal(True)

        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.label = QLabel(label)
        self.line_edit = QLineEdit()
        self.line_edit.setText(default)
        self.line_edit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9_()]*")))

        input_layout.addWidget(self.label)
        input_layout.addWidget(self.line_edit)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(input_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_text(self) -> str:
        return self.line_edit.text()
