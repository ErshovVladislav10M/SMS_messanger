from abc import ABC, abstractmethod

from Main_project.db_model import Message


class BaseProvider(ABC):
    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def update_message_status(self, message: Message):
        pass
