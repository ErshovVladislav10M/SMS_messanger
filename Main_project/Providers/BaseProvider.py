from abc import ABC, abstractmethod

from Main_project.db_model import Message


class BaseProvider(ABC):
    @staticmethod
    @abstractmethod
    def send_message():
        pass

    @staticmethod
    @abstractmethod
    def update_message_status(message: Message):
        pass
