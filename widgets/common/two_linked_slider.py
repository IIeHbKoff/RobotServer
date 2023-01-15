from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout, QSlider, QToolButton, QLabel

from common_files import Telemetry
from common_files.utils import Utils


class TwoLinkedSliders(QWidget):
    def __init__(self, text1, text2, min_value, max_value, start, telemetry_param1_name, telemetry_param2_name):
        super().__init__()
        self._telemetry = Telemetry()
        self._utils = Utils()
        
        self._layout = QGridLayout(self)
        self._telemetry_param1_name = telemetry_param1_name
        self._telemetry_param2_name = telemetry_param2_name

        self._slider1 = QSlider(Qt.Orientation(2))
        self._slider1.setSliderPosition(start)
        self._slider1.setMinimum(min_value)
        self._slider1.setMaximum(max_value)

        self._slider2 = QSlider(Qt.Orientation(2))
        self._slider2.setSliderPosition(start)
        self._slider2.setMinimum(min_value)
        self._slider2.setMaximum(max_value)

        self._button = QToolButton()
        self._button.setIcon(QIcon("assets/images/chain.png"))
        self._button.setCheckable(True)
        self._button.setMinimumSize(50, 50)

        self._label1 = QLabel(text1)
        self._label2 = QLabel(text2)
        self._percent_label1 = QLabel(f"{start}")
        self._percent_label2 = QLabel(f"{start}")

        self._slider1.valueChanged.connect(self.update_handler)
        self._slider2.valueChanged.connect(self.update_handler)

        self._layout.addWidget(self._percent_label1, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._slider1, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._label1, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._layout.addWidget(self._button, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._layout.addWidget(self._percent_label2, 0, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._slider2, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._label2, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

    def update_handler(self, value):
        sender = self.sender()
        if sender == self._slider1:
            if self._button.isChecked():
                self._slider2.setSliderPosition(value)
                self._percent_label2.setNum(value)
                self._telemetry.__setattr__(self._telemetry_param2_name, value)
            self._percent_label1.setNum(value)
            self._telemetry.__setattr__(self._telemetry_param1_name, value)
        elif sender == self._slider2:
            if self._button.isChecked():
                self._slider1.setSliderPosition(value)
                self._percent_label1.setNum(value)
                self._telemetry.__setattr__(self._telemetry_param1_name, value)
            self._percent_label2.setNum(value)
            self._telemetry.__setattr__(self._telemetry_param2_name, value)
        self._utils.send_cmds()
