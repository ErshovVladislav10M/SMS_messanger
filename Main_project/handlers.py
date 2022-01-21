import datetime
import json
import uuid

from flask import abort, render_template

from Main_project.base import app, db
from Main_project.celery_tasks import QUEUE_MESSAGES_UUID, messenger_controller
from Main_project.db_model import Message


class MyError(BaseException):
    pass


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/create-message/<username>/POST/<text_message>/<number>")
def create_message(username, text_message, number):
    message_uuid = uuid.uuid4()

    message = Message(
        message_uuid=str(message_uuid),
        created_by=username,
        created_at=datetime.datetime.now(),
        text_message=text_message,
        number=number,
    )

    try:
        db.session.add(message)
        db.session.commit()
        QUEUE_MESSAGES_UUID.append(str(message_uuid))
        messenger_controller.delay()
        return json.dumps(str(message_uuid))
    except MyError:
        return json.dumps("Error adding message")


@app.route("/message-status/<username>/GET/<message_uuid>")
def message_status(username, message_uuid):
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
        return abort(401)


@app.route("/messages-info")
def messages_info():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("messages-info.html", messages=messages)
