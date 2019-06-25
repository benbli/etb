from datetime import datetime
from battlefield import db


class Player(db.Model):
<<<<<<< HEAD
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
=======
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(25), nullable=False)
	password = db.Column(db.String(60), unique=True, nullable=False)
	time_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	#leagues = db.relationship('League', backref='leagues', lazy=True)
	#tournaments = db.relationship('Tournament', backref='tournaments', lazy=True)
	#matches_won = db.relationship('Match', backref='won', lazy=True, foreign_keys='Match.winner')
	#matches_lost = db.relationship('Match', backref='lost', lazy=True, foreign_keys='Match.loser')

	def __repr__(self):
		return f"Player('{self.id}', '{self.name}', '{self.password}')"


class Tournament(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)


class Scoreboard(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	player = db.Column(db.Integer, nullable=False)
	wins = db.Column(db.Integer, nullable=False, default=0)
	losses = db.Column(db.Integer, nullable=False, default=0)
	draws = db.Column(db.Integer, nullable=False, default=0)
	tiebreak = db.Column(db.Float, nullable=False, default=0)
	tournamentId = db.Column(db.Integer, nullable=False)



class Match(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	player1 = db.Column(db.Integer, nullable=False)
	player2 = db.Column(db.Integer, nullable=False)
	p1_game_wins = db.Column(db.Integer, nullable=False)
	p2_game_wins = db.Column(db.Integer, nullable=False)
	tournamentId = db.Column(db.Integer, nullable=False)
	time_played = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
>>>>>>> dev
