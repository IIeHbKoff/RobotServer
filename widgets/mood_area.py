from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QToolButton, QPushButton, QScrollArea, QFrame, QInputDialog

from common_files import Telemetry
from common_files.utils import FileManager
from custom_signals import custom_signals


class MoodArea(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout(self)
        self._layout.setSpacing(0)
        self._telemetry = Telemetry()
        self._label = QLabel("MoodArea")
        self._mood_creator = MoodCreator()
        self._mood_picker = MoodPicker()
        self._label.setStyleSheet("color: rgb(255, 198, 109)")
        self._layout.addWidget(self._label, 0, 0, 1, -1)
        self._layout.addWidget(self._mood_picker, 1, 0)
        self._layout.addWidget(self._mood_creator, 1, 1)


class MoodCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(280)
        self._layout = QGridLayout(self)
        self._telemetry = Telemetry()
        custom_signals.pick_mood_signal.connect(self._update_handler)
        self._matrix = Matrix()
        self._picked_mood = None
        self._save_button = QPushButton("Save")
        self._save_button.clicked.connect(self._save_handler)
        self._clear_button = QPushButton("Clear")
        self._clear_button.clicked.connect(self._clear)
        custom_signals.delete_mood_signal.connect(self._delete_mood_handler)
        self._layout.addWidget(self._matrix, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._save_button, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._clear_button, 1, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

    def _update_handler(self, e):
        self._picked_mood = e[0]
        self._matrix.show_img(e[1])

    def _save_handler(self):
        matrix = self._matrix.get_matrix()
        name = self._picked_mood
        if not name:
            name = self._show_dialog()
        if name:
            self._clear()
            custom_signals.save_mood_signal.emit((name, matrix))
    
    def _delete_mood_handler(self):
        self._picked_mood = None
    
    def _show_dialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter mood name:')
        if ok and text:
            return str(text)

    def _clear(self):
        self._picked_mood = None
        self._matrix.show_img([0, 0, 0, 0, 0, 0, 0, 0])


class Matrix(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self.setFixedHeight(220)
        self._layout = QGridLayout(self)
        self._buttons_list = [[], [], [], [], [], [], [], []]
        for curr_row in range(8):
            for curr_column in range(8):
                button = QToolButton()
                button.setCheckable(True)
                button.setFixedWidth(20)
                button.setFixedHeight(20)
                self._layout.addWidget(button, curr_row, curr_column, alignment=Qt.AlignmentFlag.AlignHCenter)
                self._buttons_list[curr_row].append(button)

    def show_img(self, data: list):
        for i, row in enumerate(self._buttons_list):
            for j, button in enumerate(row):
                button.setChecked(data[i] & (1 << (7 - j)))

    def get_matrix(self):
        res = list()
        for i, row in enumerate(self._buttons_list):
            res_number = 0
            for j, button in enumerate(row):
                if button.isChecked():
                    res_number = res_number | (1 << (7 - j))
            res.append(res_number)
        return res


class MoodPicker(QWidget):
    def __init__(self):
        super().__init__()
        self._telemetry = Telemetry()
        self._moods_file = FileManager()
        self._layout = QGridLayout(self)

        self._send_button = QPushButton("Send")
        self._delete_button = QPushButton("Delete")
        self._moods = Moods()

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidget(self._moods)
        self._scroll_area.setWidgetResizable(True)

        self._layout.addWidget(self._scroll_area, 0, 0, 8, 9, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self._send_button, 8, 0, 1, 3)
        self._layout.addWidget(self._delete_button, 8, 6, 1, 3)

        self._send_button.clicked.connect(self.send_mood)
        self._delete_button.clicked.connect(self.delete_mood)

    def send_mood(self, e):
        self._telemetry.mood = self._moods.get_picked_mood_info()

    @staticmethod
    def delete_mood(e):
        custom_signals.delete_mood_signal.emit()


class Moods(QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QGridLayout(self)
        self._moods_file = FileManager()
        self._moods = self._moods_file.read_file()
        self._pressed_button: Optional[QToolButton] = None
        self._build()
        custom_signals.delete_mood_signal.connect(self._delete_mood)
        custom_signals.save_mood_signal.connect(self._save_mood)

    def _build(self):
        self._buttons = dict()
        columns = 2
        column = 0
        row = 0
        for mood in self._moods.keys():
            btn = QToolButton()
            btn.setText(mood)
            btn.setCheckable(True)
            btn.setFixedWidth(130)
            btn.setFixedHeight(30)
            btn.clicked.connect(self._one_pressed_button_controller)
            if column == columns:
                row += 1
                column = 0
            self._layout.addWidget(btn, row, int(column))
            column += 1
            self._buttons[mood] = btn

    def _one_pressed_button_controller(self, a0):
        sender: QToolButton = self.sender()
        if self._pressed_button:
            self._pressed_button.setChecked(False)
            if self._pressed_button is sender:
                self._pressed_button = None
            else:
                self._pressed_button = sender
                self._pressed_button.setChecked(True)
        else:
            self._pressed_button = sender
            self._pressed_button.setChecked(True)
        custom_signals.pick_mood_signal.emit(
            (self._pressed_button.text(), self._moods[self._pressed_button.text()]) if self._pressed_button
            else (None, [0, 0, 0, 0, 0, 0, 0, 0]))

    def get_picked_mood_info(self):
        return self._moods[self._pressed_button.text()] if self._pressed_button else [0, 0, 0, 0, 0, 0, 0, 0]

    @property
    def picked_mood_name(self):
        return self._pressed_button.text() if self._pressed_button else None

    def _delete_mood(self):
        mood = self._pressed_button.text() if self._pressed_button else None
        if mood:
            self._moods_file.delete_row(mood)
            for btn in self._buttons.values():
                self._layout.removeWidget(btn)
            self._pressed_button = None
            self._build()

    def _save_mood(self, e):
        if e[0] in self._moods:
            self._moods_file.edit_row(e)
        else:
            self._moods_file.write_row(e)
            for btn in self._buttons.values():
                self._layout.removeWidget(btn)
            self._build()
        self._pressed_button = None
