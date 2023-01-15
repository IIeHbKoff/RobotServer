from PyQt6.QtCore import QBasicTimer, QTimerEvent, Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from common_files import Telemetry


class InfoArea(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout(self)
        self._telemetry = Telemetry()
        self._label = QLabel("InfoArea")
        self._label.setStyleSheet("color: rgb(255, 198, 109)")
        self._layout.addWidget(self._label, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self._label_list = list()
        self._timer = QBasicTimer()
        row = 1
        column = 0
        columns = 5
        for param in self._telemetry.client_params:
            label = QLabel(f"{param}:{getattr(self._telemetry, param)}")
            self._layout.addWidget(label, row, column)
            self._label_list.append(label)
            if column >= columns:
                column = 0
                row += 1
            else:
                column += 1
        self._timer.start(100, self)

    def timerEvent(self, a0: QTimerEvent) -> None:
        list_of_params = self._telemetry.get_current_telemetry()
        for index, label in enumerate(self._label_list):
            label.setText(list_of_params[index])