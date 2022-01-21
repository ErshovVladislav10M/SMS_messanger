import datetime
from pathlib import Path

from Main_project.base import db
from Main_project.db_model import Message


class FileProvider:
    name = "FileProvider"

    @staticmethod
    def send_message(message: Message):
        name_fi = (
            str(datetime.datetime.now().isoformat()).replace(":", ".")
            + "_"
            + message.number
            + ".txt"
        )
        with open(
            Path.cwd() / "Providers" / "sent_sms" / name_fi,
            "w",
        ) as fi:
            fi.write(message.text_message)

    @staticmethod
    def update_message_status(message: Message):
        message.sent_at = datetime.datetime.now()
        if int(message.number.lstrip("+")) % 2 == 0:
            message.delivered_at = message.sent_at + datetime.timedelta(
                days=0, seconds=10
            )
            message.status = "Delivered"
        else:
            message.status = "Sent"

        db.session.add(message)
        db.session.commit()
