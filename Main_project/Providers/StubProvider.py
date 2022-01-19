import datetime

from Main_project.Providers.BaseProvider import BaseProvider
from Main_project.db_model import Message
from Main_project.base import db


class StubProvider(BaseProvider):
    def send_message(self):
        pass

    def update_message_status(self, message: Message):
        message.sent_at = datetime.datetime.now()
        message.status = "Sent"
        db.session.add(message)
        db.session.commit()
