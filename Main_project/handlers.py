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


@app.route("/")
def home():
    return render_template("home.html")


@app.before_request
def authentication():
    if not request.headers.get("AUTHORIZATION"):
        abort(401)


@app.route("/create-message/<text_message>/<number>/<provider>")
def create_message(text_message: str, number: str, provider: str):
    code_str = request.headers.get("AUTHORIZATION").lstrip("Basic ")
    decode_str = b64decode(code_str)
    username = decode_str.decode("utf-8").split(":")[0]

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
        messenger_controller()
        return json.dumps(str(message_uuid))
    except MyError:
        return json.dumps("Error adding message")


@app.route("/message-status/<message_uuid>")
def message_status(message_uuid: str):
    code_str = request.headers.get("AUTHORIZATION").lstrip("Basic ")
    decode_str = b64decode(code_str)
    username = decode_str.decode("utf-8").split(":")[0]

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
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("messages-info.html", messages=messages)
