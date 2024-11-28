from enum import Enum, auto
from typing import Optional

from PyQt5.QtCore import QRectF, QSize, Qt, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPen
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSlider,
    QStyle,
    QStyleOptionSlider,
    QWidget,
)

from musa.util.image import Image


class RoundHandleSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handle_diameter = 12

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        # Get the style
        style = self.style()

        # Draw the groove
        radius = self.handle_diameter // 2
        groove_rect = style.subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self
        ).adjusted(radius, 0, -radius, 0)

        opt.subControls = QStyle.SC_SliderGroove
        opt.rect = groove_rect
        style.drawComplexControl(QStyle.CC_Slider, opt, painter, self)

        # Compute handle rect
        handle_rect = self.style().subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self
        )

        center_x = handle_rect.center().x()
        center_y = handle_rect.center().y()

        # Create circle rect
        circle_rect = QRectF(
            center_x - self.handle_diameter / 2,
            center_y - self.handle_diameter / 2,
            self.handle_diameter,
            self.handle_diameter,
        )

        # Draw the Handle
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setBrush(QBrush(QColor(220, 220, 220)))
        painter.drawEllipse(circle_rect)


class ColorChannelSlider(QSlider):
    def __init__(self, channel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = channel
        self.setMinimum(0)
        self.setMaximum(255)

        self.handle_diameter = 12

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        # Gradient
        radius = self.handle_diameter // 2
        groove_rect = (
            self.style()
            .subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
            .adjusted(radius, 0, -radius, 0)
        )
        gradient = QLinearGradient(groove_rect.left(), 0, groove_rect.right(), 0)

        # Set Colors based on channel
        if self.channel == "r":
            gradient.setColorAt(0, QColor(0, 0, 0))
            gradient.setColorAt(1, QColor(255, 0, 0))
        elif self.channel == "g":
            gradient.setColorAt(0, QColor(0, 0, 0))
            gradient.setColorAt(1, QColor(0, 255, 0))
        elif self.channel == "b":
            gradient.setColorAt(0, QColor(0, 0, 0))
            gradient.setColorAt(1, QColor(0, 0, 255))

        painter.setPen(QPen(Qt.black, 1))
        painter.fillRect(groove_rect, gradient)

        # Compute handle rect
        handle_rect = self.style().subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self
        )

        center_x = handle_rect.center().x()
        center_y = handle_rect.center().y()

        # Create circle rect
        circle_rect = QRectF(
            center_x - self.handle_diameter / 2,
            center_y - self.handle_diameter / 2,
            self.handle_diameter,
            self.handle_diameter,
        )

        # Draw the Handle
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setBrush(QBrush(QColor(220, 220, 220)))
        painter.drawEllipse(circle_rect)


class OpacitySlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimum(0)
        self.setMaximum(255)

        self.handle_diameter = 12

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        # Create checkedboard pattern
        radius = self.handle_diameter // 2
        groove_rect = (
            self.style()
            .subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
            .adjusted(radius, 0, -radius, 0)
        )

        check = Image.checker_board(QSize(groove_rect.width(), groove_rect.height()), 2)
        painter.drawPixmap(groove_rect, check)

        # Opacity gradient
        gradient = QLinearGradient(groove_rect.left(), 0, groove_rect.right(), 0)
        gradient.setColorAt(0, QColor(42, 130, 218, 255))
        gradient.setColorAt(1, QColor(42, 130, 218, 0))
        painter.setPen(QPen(Qt.black, 1))
        painter.fillRect(groove_rect, gradient)

        # Compute handle rect
        handle_rect = self.style().subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self
        )

        center_x = handle_rect.center().x()
        center_y = handle_rect.center().y()

        # Create circle rect
        circle_rect = QRectF(
            center_x - self.handle_diameter / 2,
            center_y - self.handle_diameter / 2,
            self.handle_diameter,
            self.handle_diameter,
        )

        # Draw the Handle
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setBrush(QBrush(QColor(220, 220, 220)))
        painter.drawEllipse(circle_rect)


class ValueSlider(QWidget):
    actionTriggered = pyqtSignal(int)
    rangeChanged = pyqtSignal(int, int)
    sliderMoved = pyqtSignal(int)
    sliderPressed = pyqtSignal()
    sliderReleased = pyqtSignal()
    valueChanged = pyqtSignal(int)

    class Type(Enum):
        NORMAL = auto()
        RED = auto()
        GREEN = auto()
        BLUE = auto()
        ALPHA = auto()

    def __init__(
        self,
        slider_type: Type = Type.NORMAL,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        match slider_type:
            case self.Type.NORMAL:
                self._slider = RoundHandleSlider(Qt.Horizontal, self)
            case self.Type.RED:
                self._slider = ColorChannelSlider("r", Qt.Horizontal, self)
            case self.Type.GREEN:
                self._slider = ColorChannelSlider("g", Qt.Horizontal, self)
            case self.Type.BLUE:
                self._slider = ColorChannelSlider("b", Qt.Horizontal, self)
            case self.Type.ALPHA:
                self._slider = OpacitySlider(Qt.Horizontal, self)
            case _:
                raise ValueError("Unknown Slider Type")

        self._label = QLabel("")
        self._label.setMinimumWidth(30)
        self._label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self._label.setFrameShape(QFrame.StyledPanel)
        self._label.setFrameShadow(QFrame.Sunken)
        self._label.setStyleSheet(
            "background-color: rgb(42, 42, 42); border-radius: 2px;"
        )

        self._slider.actionTriggered.connect(self.actionTriggered)
        self._slider.rangeChanged.connect(self.rangeChanged)
        self._slider.sliderMoved.connect(self.sliderMoved)
        self._slider.sliderPressed.connect(self.sliderPressed)
        self._slider.sliderReleased.connect(self.sliderReleased)
        self._slider.valueChanged.connect(self.valueChanged)

        self._slider.valueChanged.connect(lambda value: self._label.setText(f"{value}"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._slider, Qt.AlignLeft)
        layout.addStretch()
        layout.addWidget(self._label)

    @pyqtSlot(int)
    def setValue(self, value: int) -> None:
        self._slider.setValue(value)
        self._label.setText(f"{value}")

    def value(self) -> int:
        return self._slider.value()

    @pyqtSlot(int, int)
    def setRange(self, a: int, b: int) -> None:
        self._slider.setRange(a, b)

    def setSingleStep(self, step: int) -> None:
        self._slider.setSingleStep(step)

    def setTickInterval(self, interval: int) -> None:
        self._slider.setTickInterval(interval)

    def setTickPosition(self, position: QSlider.TickPosition) -> None:
        self._slider.setTickPosition(position)

    def tickPosition(self) -> QSlider.TickPosition:
        return self._slider.tickPosition()

    def setMaximum(self, max: int) -> None:
        self._slider.setMaximum(max)

    def maximum(self) -> int:
        return self._slider.maximum()

    def setMinimum(self, max: int) -> None:
        self._slider.setMinimum(max)

    def minimum(self) -> int:
        return self._slider.minimum()

    # support QDataWidgetMapper
    @pyqtProperty(int, user=True)
    def sliderValue(self) -> int:
        return self.value()

    @sliderValue.setter
    def sliderValue(self, value: int) -> None:
        self._slider.setValue(value)
        self.valueChanged.emit(value)
