from abc import ABC, abstractmethod


class BaseSkill(ABC):

    @abstractmethod
    def run(self, params: str) -> str:
        """

        @param params: str
        @return: str
        """

    @property
    @abstractmethod
    def skill_tag(self) -> str:
        """
        @return: str
        """

    @abstractmethod
    def _create_request_packet(self) -> str:
        """

        @return: str
        """
