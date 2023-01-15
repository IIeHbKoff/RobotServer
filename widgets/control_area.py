from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from common_files import Telemetry
from widgets.common.two_linked_slider import TwoLinkedSliders
from widgets.common.my_slider import MySlider


class ControlArea(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout(self)
        self._telemetry = Telemetry()
        self._label = QLabel("ControlArea")
        self._label.setStyleSheet("color: rgb(255, 198, 109)")
        self._layout.addWidget(self._label, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self._move_Sliders = TwoLinkedSliders("RWS", "LWS", -100, 100, 0, "rws", "lws")
        self._servo0_Slider = MySlider("servo0", -90, 90, 0, "sch0")
        self._servo1_Slider = MySlider("servo1", -90, 90, 0, "sch1")
        self._servo2_Slider = MySlider("servo2", -90, 90, 0, "sch2")
        self._servo3_Slider = MySlider("servo3", -90, 90, 0, "sch3")
        self._servo4_Slider = MySlider("servo4", -90, 90, 0, "sch4")
        self._servo5_Slider = MySlider("servo5", -90, 90, 0, "sch5")
        self._servo6_Slider = MySlider("servo6", -90, 90, 0, "sch6")
        self._servo7_Slider = MySlider("servo7", -90, 90, 0, "sch7")

        self._layout.addWidget(self._move_Sliders, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._servo0_Slider, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._servo1_Slider, 1, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._servo2_Slider, 1, 4, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._servo3_Slider, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._servo4_Slider, 2, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._servo5_Slider, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._servo6_Slider, 2, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._servo7_Slider, 2, 4, alignment=Qt.AlignmentFlag.AlignHCenter)
