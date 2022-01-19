import datetime
import uuid

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


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


@app.route("/message-status/<int:message_uuid>")
def message_status(message_uuid: str):
    message = Message.query.get(message_uuid)
    return render_template("message-status.html", message=message)


@app.route("/messages-info", methods=["POST", "GET"])
def messages_info():
    if request.method == "POST":
        message_uuid = request.form["message_uuid"]
        return redirect("/message-status/" + str(message_uuid))
    else:
        return render_template("messages-info.html")


@app.route("/create-message", methods=["POST", "GET"])
def create_message():
    if request.method == "POST":
        text_message = request.form["text_message"]
        number = request.form["number"]
        provider = request.form["provider"]
        message_uuid = uuid.uuid4()

        message = Message(
            message_uuid=str(message_uuid),
            text_message=text_message,
            number=number,
            provider=provider,
        )

        try:
            db.session.add(message)
            db.session.commit()
            #return redirect("/messages-info")
            return redirect("/message-status/" + str(message_uuid))
        except:
            return "Error adding message"
    else:
        return render_template("create-message.html")


if __name__ == "__main__":
    app.run(debug=True)
