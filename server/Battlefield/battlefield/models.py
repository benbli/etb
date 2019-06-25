from datetime import datetime
from battlefield import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #leagues = db.relationship('League', backref='leagues', lazy=True)
    #tournaments = db.relationship('Tournament', backref='tournaments', lazy=True)
    #matches = db.relationship('Game', backref='matches', lazy=True)

    def __repr__(self):
        return f"Player('{self.id}', '{self.first_name}', '{self.last_name}', '{self.password}')"


class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
