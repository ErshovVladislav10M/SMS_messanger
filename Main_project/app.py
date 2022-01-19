import datetime
import json
import uuid

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class MyError(BaseException):
    pass


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_uuid = db.Column(db.String(50), unique=True)
    text_message = db.Column(db.String(140), nullable=False)
    number = db.Column(db.String(11), nullable=False)
    provider = db.Column(db.String(140), default="StubProvider")
    is_sent = db.Column(db.Integer, default=0)
    is_delivered = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return "<Message %r>" % self.id


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


if __name__ == "__main__":
    app.run(debug=True)
