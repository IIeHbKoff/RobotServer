from actual_state import ActualState
from common_files.constants import Constants
from skills.interface import BaseSkill
import pygame


class MovementSkill(BaseSkill):
    _instance = None
    _driver = None
    _state = None

    class_name = __qualname__
    skill_tag = Constants.MOVEMENT_SKILL_TAG
    buttons_dict = {
        0b0000: (0, 0),
        0b1000: (50, 50),
        0b0100: (-50, -50),
        0b0010: (50, 0),
        0b0001: (0, 50),
        0b1001: (50, 75),
        0b1010: (75, 50),
        0b0110: (-75, -50),
        0b0101: (-50, -75),
        0b1100: (-50, 50),
        0b0011: (50, -50),
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MovementSkill, cls).__new__(cls)
            cls._state = ActualState()
        return cls._instance

    def run(self, keys=None, coords=None):
        if keys is not None:
            var = (0b1000 if pygame.K_UP in keys else 0b0000) | (0b0100 if pygame.K_DOWN in keys else 0b0000) | \
                  (0b0010 if pygame.K_LEFT in keys else 0b0000) | (0b0001 if pygame.K_RIGHT in keys else 0b0000)
            try:
                buttons_tuple = self.buttons_dict[var]
                self._state.left_wheel = buttons_tuple[0]
                self._state.right_wheel = buttons_tuple[1]
            except KeyError:
                self._state.left_wheel = 0
                self._state.right_wheel = 0
            return self._create_request_packet()
        elif coords is not None:
            pass
        else:
            self._create_request_packet()

    def _create_request_packet(self) -> str:
        return f"{self.skill_tag}:{self._state.left_wheel},{self._state.right_wheel}"
