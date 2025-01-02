from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15),  nullable=False)
    messages = db.relationship('ScheduledMessage', back_populates='client', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name}, phone={self.phone})>"

class ScheduledMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', back_populates='messages')  # Relacionamento explícito
    message = db.Column(db.Text, nullable=False)
    schedule_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<ScheduledMessage(id={self.id}, client={self.client.name}, schedule_time={self.schedule_time})>"

class MessageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    status = db.Column(db.String(20))  # Sucesso ou Falha
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<MessageLog(id={self.id}, client_id={self.client_id}, status={self.status}, timestamp={self.timestamp})>"
