from common_files import Telemetry
from common_files.constants import Constants
from skills.interface import BaseSkill


class MovementSkill(BaseSkill):
    _instance = None
    _telemetry = None

    class_name = __qualname__
    skill_tag = Constants.MOVEMENT_SKILL_TAG

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MovementSkill, cls).__new__(cls)
            cls._telemetry = Telemetry()
        return cls._instance

    def run(self):
        return self._create_request_packet()

    def _create_request_packet(self) -> str:
        return f"{self.skill_tag}:{self._telemetry.lws},{self._telemetry.rws}"
