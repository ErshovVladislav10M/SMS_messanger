import datetime

from Main_project.base import db
from Main_project.db_model import Message


class StubProvider:
    name = "StubProvider"

    @staticmethod
    def send_message(message: Message):
        pass

    @staticmethod
    def update_message_status(message: Message):
        message.sent_at = datetime.datetime.now()
        message.status = "Sent"
        db.session.add(message)
        db.session.commit()
