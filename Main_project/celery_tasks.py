import time

from Main_project.base import celery
from Main_project.db_model import Message
from Main_project.Providers.FileProvider import FileProvider
from Main_project.Providers.StubProvider import StubProvider

LIST_PROVIDERS = [StubProvider, FileProvider]
QUEUE_MESSAGES_UUID = []


@celery.task
def messenger_controller():
    """
    Sending messages from the unsent queue by the respective providers.
    """
    while len(QUEUE_MESSAGES_UUID) > 0:
        message_uuid = QUEUE_MESSAGES_UUID.pop()
        message = Message.query.filter_by(message_uuid=message_uuid).first()

        for provider in LIST_PROVIDERS:
            if provider.name == message.provider:
                attempt = 1
                while provider.numbers_of_attempt_send >= attempt:
                    if provider.send_message(message):
                        break
                    attempt += 1
                    time.sleep(provider.repeat_time)

                provider.update_message_status(message)
                break
