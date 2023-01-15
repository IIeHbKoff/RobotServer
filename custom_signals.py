from PyQt6.QtCore import QObject, pyqtSignal


class CustomSignals(QObject):
    pick_mood_signal = pyqtSignal(tuple)
    delete_mood_signal = pyqtSignal()
    save_mood_signal = pyqtSignal(tuple)


custom_signals = CustomSignals()
