import datetime
import json
import uuid
from base64 import b64decode

from flask import abort, render_template, request

from Main_project.base import app, db
from Main_project.celery_tasks import QUEUE_MESSAGES_UUID, messenger_controller
from Main_project.db_model import Message


class MyError(BaseException):
    pass


@app.before_request
def authentication():
    """
    Checking for the presence of an HTTP header
    and the correctness of its format.
    """
    if not request.headers.get("AUTHORIZATION"):
        abort(401)
    elif request.headers.get("AUTHORIZATION").split()[0] != "Basic":
        abort(401)


def get_username_from_http():
    """
    Getting username from HTTP header.
    """
    code_str = request.headers.get("AUTHORIZATION").lstrip("Basic ")
    decode_str = b64decode(code_str)
    return decode_str.decode("utf-8").split(":")[0]


@app.route("/create-message/<text_message>/<number>/<provider>")
def create_message_add_to_db(text_message: str, number: str, provider: str):
    """
    Creating an instance of the Message class
    and inserting it into the database.
    Returns the uuid of the generated message, if successful.
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

    try:
        db.session.add(message)
        db.session.commit()
        QUEUE_MESSAGES_UUID.append(str(message_uuid))
        messenger_controller.delay()
        return json.dumps(str(message_uuid))
    except MyError:
        return json.dumps("Error adding message")


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


@app.route("/messages-info")
def messages_info():
    """
    Helper function for debugging, returns information about all messages.
    """
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("messages-info.html", messages=messages)
