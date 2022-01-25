from abc import ABC, abstractmethod

from Main_project.db_model import Message


class BaseProvider(ABC):
    @staticmethod
    @abstractmethod
    def send_message(message: Message):
        """
        Performing actions on the message that correspond
        to the functionality of the provider.
        Returns True if the submission was successful.
        """

    @staticmethod
    @abstractmethod
    def update_message_status(message: Message):
        """
        Updating the status of a message in the database.
        """
