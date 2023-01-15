from PyQt6.QtCore import QBasicTimer, QTimerEvent
from PyQt6.QtGui import QPainter, QPaintEvent, QMouseEvent, QColor
from PyQt6.QtWidgets import QFrame

from common_files.utils import Utils


class DrawingArea(QFrame):
    def __init__(self):
        super().__init__()
        self._painter = QPainter()
        self._timer = QBasicTimer()
        self._timer.start(1, self)
        self._points = list()
        self.curr_pos_x = 0
        self.curr_pos_y = 0
        self.curr_direction = 0
        self._utils = Utils()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print("press " + a0.pos().x().__str__() + ", " + a0.pos().y().__str__())

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        print("release " + a0.pos().x().__str__() + ", " + a0.pos().y().__str__())

    def paintEvent(self, a0: QPaintEvent):
        self._painter.begin(self)
        self._painter.setPen(QColor(255, 255, 255))
        self._painter.drawLine(self.curr_pos_x, self.curr_pos_y, self.curr_pos_x+10, self.curr_pos_y+10)
        if self._points:
            self._painter.setPen(QColor(255, 0, 0))
            for x, y in self._points:
                self._painter.drawPoint(x, y)
        self._painter.end()

    def timerEvent(self, a0: QTimerEvent) -> None:
        self._points = self._utils.calculate_points()
        self.update()
