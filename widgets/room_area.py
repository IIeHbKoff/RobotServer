from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from widgets.drawing_area import DrawingArea


class RoomArea(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout(self)
        self._label = QLabel("RoomArea")
        self._frame = DrawingArea()
        self._frame.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')
        self._frame.setMinimumSize(700, 700)
        self._frame.setMaximumSize(700, 700)
        self._label.setStyleSheet("color: rgb(255, 198, 109)")
        self._layout.addWidget(self._label, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self._layout.addWidget(self._frame, 1, 0, 30, 10, alignment=Qt.AlignmentFlag.AlignTop)
