from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListView,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AnimationListModel(QAbstractListModel):
    def __init__(self, data_model, parent=None):
        super().__init__(parent)
        self.data_model = data_model

    def rowCount(self, parent=QModelIndex()):
        return len(self.data_model.get_animations())

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        animation = self.data_model.get_animations()[index.row()]

        if role == Qt.DisplayRole:
            return animation.name

        return None


class AnimationListWidget(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.data_model = model
        self.animation_model = AnimationListModel(self.data_model)
        self.list.setModel(self.animation_model)

    def setup_ui(self):
        layout = QVBoxLayout()

        title_lay = QHBoxLayout()
        self.title = QLabel("Animations")
        title_lay.addWidget(self.title)

        list_lay = QVBoxLayout()
        self.list = QListView()
        list_lay.addWidget(self.list)

        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignTop)
        self.add_btn = QPushButton("+")
        self.del_btn = QPushButton("-")
        self.add_btn.setFixedSize(32, 32)
        self.del_btn.setFixedSize(32, 32)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.del_btn)

        hbox = QHBoxLayout()
        hbox.addLayout(list_lay)
        hbox.addLayout(btn_layout)

        layout.addLayout(title_lay)
        layout.addLayout(hbox)

        self.setLayout(layout)
