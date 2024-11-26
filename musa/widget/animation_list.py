from typing import Any, List
from uuid import UUID

from PyQt5.QtCore import (
    QAbstractListModel,
    QItemSelectionModel,
    QModelIndex,
    Qt,
    pyqtSignal,
)
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QPushButton,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
)

from musa.dialog import FileDialogFactory
from musa.model.animation import Animation
from musa.model.animation_collection import AnimationCollection


class AnimationItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index: QModelIndex):
        editor = QLineEdit(parent)
        editor.setText(index.data(Qt.UserRole))
        return editor

    def setEditorData(self, editor: QLineEdit, index: QModelIndex):
        value = index.model().data(index, Qt.EditRole)
        editor.setText(value)

    def setModelData(
        self, editor: QLineEdit, model: QAbstractListModel, index: QModelIndex
    ):
        value = editor.text()
        model.setData(index, value, Qt.UserRole)


class AnimationListModel(QAbstractListModel):
    def __init__(self, collection: AnimationCollection, parent=None):
        super().__init__(parent)
        self.collection = collection
        self.animations: List[UUID] = []

        # connect to collection signals
        self.collection.signals.animationAdded.connect(self._on_animation_added)
        self.collection.signals.animationRemoved.connect(self._on_animation_removed)
        self.collection.signals.collectionLoaded.connect(self._on_collection_loaded)

        # Initialize data
        self._refresh_animations_list()

    def _refresh_animations_list(self):
        self.animations = [anim.id for anim in self.collection.list_animations()]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.animations)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index) | Qt.ItemIsEditable

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid() or not 0 <= index.row() < len(self.animations):
            return None

        animation_id = self.animations[index.row()]
        animation = self.collection.get_animation(animation_id)

        if role == Qt.DisplayRole:
            return animation.name
        elif role == Qt.UserRole:
            return str(animation_id)

        return None

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or not 0 <= index.row() < len(self.animations):
            return False

        if role == Qt.UserRole:
            id = self.animations[index.row()]

            # Change name on all frames
            anim = self.collection.get_animation(id)
            for i, frame in enumerate(anim.frames):
                anim.update_frame(frame.id, name=f"{value.upper()} {i}")

            self.collection.update_animation(id, name=value)
            self.dataChanged.emit(index, index)
            return True

        return False

    def _on_animation_added(self, animation_id: UUID):
        position = len(self.animations)
        self.beginInsertRows(QModelIndex(), position, position)
        self._refresh_animations_list()
        self.endInsertRows()

    def _on_animation_removed(self, animation_id: UUID):
        try:
            position = self.animations.index(animation_id)
            self.beginRemoveRows(QModelIndex(), position, position)
            self._refresh_animations_list()
            self.endRemoveRows()
        except ValueError:
            pass  # Animation not in list

    def _on_collection_loaded(self):
        self.beginResetModel()
        self._refresh_animations_list()
        self.endResetModel()


class AnimationListWidget(QWidget):
    animationSelected = pyqtSignal(Animation)

    def __init__(self, collection: AnimationCollection, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.collection = collection
        self.animation_model = AnimationListModel(self.collection)
        self.list.setModel(self.animation_model)

        # connections
        self.add_btn.clicked.connect(self._on_add_animation)
        self.del_btn.clicked.connect(self._on_del_animation)
        self.list.selectionModel().currentChanged.connect(self._on_animation_selected)

    def setup_ui(self):
        layout = QVBoxLayout()

        title_lay = QHBoxLayout()
        self.title = QLabel("Animations")
        title_lay.addWidget(self.title)

        list_lay = QVBoxLayout()
        self.list = QListView()
        self.list.setItemDelegate(AnimationItemDelegate())
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

    def _on_add_animation(self):
        name = FileDialogFactory.name_input("New Animation", "Name:")
        if name:
            self.collection.create_animation(name.upper())

    def _on_del_animation(self):
        pass

    def _on_animation_selected(self, current: QItemSelectionModel, previous):
        index = current.row() if current.isValid() else -1
        id = self.animation_model.animations[index]
        animation = self.collection.get_animation(id)
        self.animationSelected.emit(animation)
