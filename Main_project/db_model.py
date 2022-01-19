import datetime

from Main_project.base import db


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
