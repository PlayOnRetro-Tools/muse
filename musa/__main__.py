import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qtmodern import styles

from musa.manager import ResourceManager
from musa.view import MusaMainWindow as Win


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    app.setWindowIcon(ResourceManager.get_icon("musa_64"))
    app.setApplicationName("M.U.S.E")
    styles.dark(app)

    window = Win()
    window.setWindowIcon(ResourceManager.get_icon("musa_64"))
    window.setWindowRole("M.U.S.E")

    desktop = QApplication.desktop().screenGeometry(0)
    window.move(desktop.left(), desktop.top())
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
