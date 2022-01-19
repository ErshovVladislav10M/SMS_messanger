import datetime

from Main_project.base import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_uuid = db.Column(db.String(50), unique=True)
    created_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    text_message = db.Column(db.String(140), nullable=False)
    number = db.Column(db.String(11), nullable=False)
    provider = db.Column(db.String(140), default="StubProvider")
    sent_at = db.Column(db.DateTime, default=None)
    delivered_at = db.Column(db.DateTime, default=None)
    status = db.Column(db.String(100), default="Accepted for shipping")

    def __repr__(self):
        return "<Message %r>" % self.id
