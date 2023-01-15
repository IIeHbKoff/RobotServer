from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QSlider, QLabel

from common_files import Telemetry
from common_files.utils import Utils


class MySlider(QWidget):
    def __init__(self, text, min_value, max_value, start, telemetry_param_name):
        super().__init__()
        self._utils = Utils()
        self._telemetry = Telemetry()

        self._layout = QGridLayout(self)
        self._telemetry_param_name = telemetry_param_name
        self._slider = QSlider(Qt.Orientation(2))
        self._slider.setSliderPosition(start)
        self._slider.setMinimum(min_value)
        self._slider.setMaximum(max_value)
        self._label = QLabel(text)
        self._percent_label = QLabel(f"{start}")
        self._slider.valueChanged.connect(self.update_handler)

        self._layout.addWidget(self._percent_label, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._slider, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._label, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

    def update_handler(self, value):
        self._percent_label.setNum(value)
        self._telemetry.__setattr__(self._telemetry_param_name, value)
        self._utils.send_cmds()
