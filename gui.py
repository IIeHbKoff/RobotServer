from PyQt6.QtCore import QBasicTimer, QTimerEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QGridLayout

from common_files import Constants
from common_files.utils import Utils
from widgets import RoomArea, InfoArea, ControlArea, MoodArea


class GUI(QDialog):
    def __init__(self):
        super().__init__()
        self._utils = Utils()
        self._utils.connect()

        self.setGeometry(0, 0, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.setWindowTitle('RobotPower')
        self.setWindowIcon(QIcon('assets/images/icon.png'))

        self._layout = QGridLayout(self)

        self._timer = QBasicTimer()

        self._room_area = RoomArea()
        self._info_area = InfoArea()
        self._control_area = ControlArea()
        self._mood_area = MoodArea()

        self._layout.addWidget(self._room_area, 1, 0, 3, 1)
        self._layout.addWidget(self._info_area, 1, 1)
        self._layout.addWidget(self._control_area, 2, 1)
        self._layout.addWidget(self._mood_area, 3, 1)

        self.show()
        self._timer.start(100, self)

    def timerEvent(self, a0: QTimerEvent):
        self._utils.get_and_fill_telemetry()
        self._utils.send_cmds()
