import datetime
import json
import uuid
from base64 import b64decode

from flask import abort, request

from Main_project.base import app, db
from Main_project.celery_tasks import QUEUE_MESSAGES_UUID, messenger_controller
from Main_project.db_model import Message

app = app


class MyError(BaseException):
    pass


def get_headers_authorization():
    """
    Getting the Authorization HTTP Header.
    """
    return request.headers.get("AUTHORIZATION")


@app.before_request
def authentication():
    """
    Checking for the presence of an HTTP header
    and the correctness of its format.
    """
    if not get_headers_authorization():
        return abort(401)
    elif get_headers_authorization().split()[0] != "Basic":
        return abort(401)


def get_username_from_http():
    """
    Getting username from HTTP header.
    """
    code_str = get_headers_authorization().lstrip("Basic ")
    decode_str = b64decode(code_str)
    return decode_str.decode("utf-8").split(":")[0]


def create_message(text_message: str, number: str, provider="StubProvider"):
    """
    Returns the created instance of the Message class.
    """
    username = get_username_from_http()
    message_uuid = uuid.uuid4()

    message = Message(
        message_uuid=str(message_uuid),
        created_by=username,
        created_at=datetime.datetime.now(),
        text_message=text_message,
        number=number,
        provider=provider,
    )

    return message


def add_message_to_db(message):
    """
    Adding an instance of the Message class to the database.
    """
    try:
        db.session.add(message)
        db.session.commit()
        QUEUE_MESSAGES_UUID.append(message.message_uuid)
        messenger_controller.delay()
        return json.dumps(message.message_uuid)
    except MyError:
        return json.dumps("Error adding message")


@app.route("/create-message/<text_message>/<number>/<provider>")
def create_mes_by_user(text_message: str, number: str, provider: str):
    """
    Creating an instance of the Message class
    and inserting it into the database.
    Returns the uuid of the generated message, if successful.
    """
    message = create_message(text_message, number, provider)
    return add_message_to_db(message)


@app.route("/create-message/<text_message>/<number>")
def create_mes_by_user_without_provider(text_message: str, number: str):
    """
    Creating an instance of the message class and
    inserting into the database with the choice of the default provider
    Returns the uuid of the generated message, if successful.
    """
    message = create_message(text_message, number)
    return add_message_to_db(message)


@app.route("/message-status/<message_uuid>")
def message_status(message_uuid: str):
    """
    By uuid of the message, it gives information
    about it from the database in json format.
    If the username from the HTTP header does not
    match the creator of the post, then code 403.
    """
    username = get_username_from_http()
    message = Message.query.filter_by(message_uuid=message_uuid).first()
    if message.created_by == username:
        data = {
            "uuid": message.message_uuid,
            "created_by": message.created_by,
            "created_at": str(message.created_at),
            "text_message": message.text_message,
            "number": message.number,
            "provider": message.provider,
            "sent_at": str(message.sent_at),
            "delivered_at": str(message.delivered_at),
            "status": message.status,
        }
        return json.dumps(data)
    else:
        return abort(403)
