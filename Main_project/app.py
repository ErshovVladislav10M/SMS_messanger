import json
import uuid

from flask import render_template

from Main_project.base import app, db
from Main_project.db_model import Message


class MyError(BaseException):
    pass


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/create-message/POST/<text_message>/<number>")
def create_message(text_message, number):
    message_uuid = uuid.uuid4()

    message = Message(
        message_uuid=str(message_uuid),
        text_message=text_message,
        number=number,
    )

    try:
        db.session.add(message)
        db.session.commit()
        return json.dumps(str(message_uuid))
    except MyError:
        return json.dumps("Error adding message")


@app.route("/message-status/GET/<message_uuid>")
def message_status(message_uuid):
    message = Message.query.filter_by(message_uuid=message_uuid).first()
    data = (
        message.message_uuid,
        message.text_message,
        message.number,
        message.is_sent,
        message.is_delivered,
    )
    return json.dumps(data)


@app.route("/messages-info")
def messages_info():
    messages = Message.query.order_by(Message.date.desc()).all()
    return render_template("messages-info.html", messages=messages)
