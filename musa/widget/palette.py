from pathlib import Path
from typing import List

from PyQt5.QtCore import QMimeData, QPoint, Qt
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from musa.dialog import FileDialogFactory, SpriteSheetDialog


class DragableSpriteLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.sprite_pixmap = pixmap
        self.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.setFixedSize(64, 64)
        self.setFrameStyle(QFrame.Box)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setImageData(self.sprite_pixmap.toImage())
            drag.setMimeData(mime_data)
            drag.setPixmap(self.sprite_pixmap.scaled(32, 32, Qt.KeepAspectRatio))
            drag.setHotSpot(QPoint(16, 16))
            drag.exec_()


class SpritePaletteWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sprite_sheets = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        toolbar = QToolBar()
        add_action = QAction("Add Sheet", self)
        add_action.triggered.connect(self.add_sprite_sheet)
        toolbar.addAction(add_action)

        remove_action = QAction("Remove Sheet", self)
        remove_action.triggered.connect(self.remove_sprite_sheet)
        toolbar.addAction(remove_action)
        layout.addWidget(toolbar)

        self.row_scroll = QScrollArea()
        self.row_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.row_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.content = QWidget()
        self.row_layout = QHBoxLayout(self.content)
        self.row_scroll.setWidget(self.content)
        self.row_scroll.setWidgetResizable(True)
        layout.addWidget(self.row_scroll)

    def add_sprite_sheet(self):
        file = FileDialogFactory.open_image()
        if file:
            extractor = SpriteSheetDialog(file, self)
            if extractor.exec_() == QFileDialog.Accepted:
                self.load_sprites(file, extractor.get_sprites())

    def load_sprites(self, file: Path, sprites: List[QPixmap]):
        sheet_widget = QWidget()
        sheet_layout = QVBoxLayout(sheet_widget)
        sheet_layout.addWidget(QLabel(file.name))

        # Arrange sprites in a column
        sprite_column = QFrame()
        column_layout = QVBoxLayout(sprite_column)
        column_layout.setSpacing(1)
        column_scroll = QScrollArea()
        column_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        column_scroll.setWidget(sprite_column)
        column_scroll.setWidgetResizable(True)

        sprite_list = []
        for sprite_pixmap in sprites:
            sprite_label = DragableSpriteLabel(sprite_pixmap)
            column_layout.addWidget(sprite_label)
            sprite_list.append(sprite_label)

        column_layout.addStretch()
        sheet_layout.addWidget(column_scroll)
        self.row_layout.addWidget(sheet_widget)
        self.sprite_sheets[file.name] = (sheet_widget, sprite_list)

    def remove_sprite_sheet(self):
        pass
