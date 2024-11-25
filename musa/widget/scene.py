from PyQt5.QtCore import QLineF, QPoint, QPointF, QRectF, QSize, Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QSizePolicy

from musa.item import SpriteItem


class EditorGrid:
    __backGridColor = QColor("#080808")
    __foreGridColor = QColor(210, 210, 210, 200)
    __darkColor = QColor("#323232")
    __lightColor = QColor("#505050")

    def __init__(self, view: QGraphicsView, size: int = 32) -> None:
        self.view = view
        self.frame_size = QSize(256, 224)
        self.grid_size = size
        self.view.drawForeground = self.drawForeground
        self.view.drawBackground = self.drawBackground

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setPen(QPen(Qt.NoPen))

        left = int(rect.left() - rect.left() % self.grid_size)
        top = int(rect.top() - rect.top() % self.grid_size)

        for y in range(top, int(rect.bottom()), self.grid_size):
            for x in range(left, int(rect.right()), self.grid_size):
                is_dark = (x / self.grid_size + y / self.grid_size) % 2

                color = self.__darkColor if is_dark else self.__lightColor
                painter.fillRect(
                    QRectF(x, y, self.grid_size, self.grid_size), QBrush(color)
                )

        l = rect.left()
        r = rect.right()
        t = rect.top()
        b = rect.bottom()

        # center visual indicator
        lines = [QLineF(l, 0, r, 0), QLineF(0, t, 0, b)]

        pen = QPen(self.__backGridColor, 0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(*lines)
        pen.setColor(self.__foreGridColor)
        painter.setPen(pen)

        # Viewport rectangle
        painter.drawRect(
            QRectF(
                -self.frame_size.width() / 2,
                -self.frame_size.height() / 2,
                self.frame_size.width(),
                self.frame_size.height(),
            )
        )

    def drawForeground(self, painter: QPainter, rect) -> None:
        start = 6
        end = 2
        lines = [
            QLineF(-start, 0, -end, 0),
            QLineF(0, -start, 0, -end),
            QLineF(end, 0, start, 0),
            QLineF(0, start, 0, end),
        ]

        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.__foreGridColor, 2, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(*lines)
        painter.drawEllipse(QPointF(0, 0), 1, 1)


class EditorScene(QGraphicsScene):
    _SIZE = 256

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(-self._SIZE / 2, -self._SIZE / 2, self._SIZE, self._SIZE)
        self.selectionChanged.connect(self._on_selection_change)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasImage():
            image = QImage(event.mimeData().imageData())

            # Convert the event to scene coordinates
            pos = event.scenePos()

            # Create the sprite item
            offset_x = image.size().width() // 2
            offset_y = image.size().height() // 2

            item = SpriteItem(QPixmap.fromImage(image))
            item.setPos(pos - QPoint(offset_x, offset_y))

            self.addItem(item)

            event.acceptProposedAction()

    def _on_selection_changed(self):
        pass


class EditorView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setAcceptDrops(True)

        # Configure the view
        self.setRenderHint(QPainter.Antialiasing)
        self.centerOn(0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.grid = EditorGrid(self)
