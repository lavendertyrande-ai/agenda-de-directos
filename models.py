from db import db

class TwitchUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitch_id = db.Column(db.String(80), unique=True, nullable=False)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitch_id = db.Column(db.String(80), nullable=False)
    hora1 = db.Column(db.String(20))
    hora2 = db.Column(db.String(20))
    hora3 = db.Column(db.String(20))

