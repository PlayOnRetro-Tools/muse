import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qtmodern import styles
from view import MusaMainWindow as Win


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    styles.dark(app)

    window = Win()
    desktop = QApplication.desktop().screenGeometry(0)
    window.move(desktop.left(), desktop.top())
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()