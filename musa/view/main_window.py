from PyQt5.QtWidgets import QMainWindow

from musa.dialog import FileDialogFactory, SpriteSheetDialog


class MusaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Musa")
        self.setup_ui()

        file = FileDialogFactory.open_image()
        if file:
            dialog = SpriteSheetDialog(file, self)
            dialog.exec_()

    def setup_ui(self):
        pass
