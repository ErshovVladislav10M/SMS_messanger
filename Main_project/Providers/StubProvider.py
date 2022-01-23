import datetime

from Main_project.base import db
from Main_project.db_model import Message


class StubProvider:
    name = "StubProvider"
    numbers_of_attempt_send = 1

    @staticmethod
    def send_message(message: Message):
        """
        Performing actions on the message that correspond
        to the functionality of the provider.
        """
        return True

    @staticmethod
    def update_message_status(message: Message):
        """
        Updating the status of a message in the database.
        """
        message.sent_at = datetime.datetime.now()
        message.delivered_at = datetime.datetime.now()
        message.status = "Is delivered"
        db.session.add(message)
        db.session.commit()
