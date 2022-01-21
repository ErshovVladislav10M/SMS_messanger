from Main_project.base import celery
from Main_project.db_model import Message
from Main_project.Providers.StubProvider import StubProvider
from Main_project.Providers.FileProvider import FileProvider

LIST_PROVIDERS = [StubProvider, FileProvider]
QUEUE_MESSAGES_UUID = []


@celery.task
def messenger_controller():
    while len(QUEUE_MESSAGES_UUID) > 0:
        message_uuid = QUEUE_MESSAGES_UUID.pop()
        message = Message.query.filter_by(message_uuid=message_uuid).first()

        for provider in LIST_PROVIDERS:
            if provider.name == message.provider:
                provider.send_message(message)
                provider.update_message_status(message)
                break
