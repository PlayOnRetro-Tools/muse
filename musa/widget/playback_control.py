from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSpinBox, QWidget


class PlayBackWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.play_btn = QPushButton("Play")
        self.play_btn.setCheckable(True)
        self.stop_btn = QPushButton("Stop")
        self.prev_btn = QPushButton("<")
        self.next_btn = QPushButton(">")

        self.fps_label = QLabel("Fps:")
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 60)
        self.fps_spin.setValue(16)

        container = QFrame()
        container.setFrameStyle(QFrame.StyledPanel)
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.next_btn)
        control_layout.addWidget(self.fps_label)
        control_layout.addWidget(self.fps_spin)
        container.setLayout(control_layout)

        layout = QHBoxLayout()
        layout.addStretch(2)
        layout.addWidget(container)
        layout.addStretch(2)
        self.setLayout(layout)
