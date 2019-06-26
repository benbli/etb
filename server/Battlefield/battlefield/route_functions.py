from flask import render_template, request, jsonify, redirect, url_for
from battlefield import app, db, bcrypt
from battlefield.models import Player, Scoreboard, Match, Tournament
from battlefield.forms import TournamentForm, RegisterForm



@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		new_player = Player(name=form.username.data, password=hashed_password)
		db.session.add(new_player)
		db.session.commit()

		return redirect(url_for('get_all_players'))
	return render_template('register.html', form=form)



@app.route("/create_tournament", methods=['GET', 'POST'])
def create_tournament():
    form = TournamentForm()
    if form.validate_on_submit():
        new_tournament = Tournament(name=form.name.data)
        db.session.add(new_tournament)
        db.session.commit()
        return 'success'
    return render_template('create_tournament.html', form=form)