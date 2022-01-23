import datetime
from pathlib import Path

from Main_project.base import db
from Main_project.db_model import Message


class FileProvider:
    name = "FileProvider"
    numbers_of_attempt_send = 3

    @staticmethod
    def send_message(message: Message):
        """
        Performing actions on the message that correspond
        to the functionality of the provider.
        Returns True if the submission was successful.
        """
        if int(message.number[-1]) % 2 != 0:
            return False

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

        return True

    @staticmethod
    def update_message_status(message: Message):
        """
        Updating the status of a message in the database.
        """
        message.sent_at = datetime.datetime.now()
        if int(message.number[-1]) % 2 == 0:
            message.delivered_at = message.sent_at + datetime.timedelta(
                days=0, seconds=10
            )
            message.status = "Is delivered"
        else:
            message.status = "Sent"

        db.session.add(message)
        db.session.commit()
