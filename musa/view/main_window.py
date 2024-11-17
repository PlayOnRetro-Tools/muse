from PyQt5.QtWidgets import QMainWindow


class MusaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Musa")
        self.setup_ui()

    def setup_ui(self):
        pass
