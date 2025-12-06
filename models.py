from db import db

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitch_id = db.Column(db.String(50), nullable=False)
    hora1 = db.Column(db.String(20), nullable=True)
    hora2 = db.Column(db.String(20), nullable=True)
    hora3 = db.Column(db.String(20), nullable=True)

class TwitchUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitch_id = db.Column(db.String(50), unique=True, nullable=False)


