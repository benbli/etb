from flask import render_template, request, jsonify, redirect, url_for
from battlefield import app, db, bcrypt
from battlefield.models import Player, Scoreboard, Match, Tournament
from battlefield.forms import TournamentForm, RegisterForm, StatisticsForm
from sqlalchemy import or_



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
    numofplayers = form.numofplayers.data

    if form.validate_on_submit():
        new_tournament = Tournament(name=form.name.data)
        db.session.add(new_tournament)
        db.session.commit()

        players = Player.query.filter(Player.id <= numofplayers)
        player_list = []

        for player in players:
            player_list.append(player.name)

        random.shuffle(player_list)

        return jsonify(player_list)

return render_template('create_tournament.html', form=form)




@app.route("/view_stats", methods=['GET', 'POST'])
def view_stats():
	form = StatisticsForm()
	if form.is_submitted():
		player_id = 0

		#FIX WHEN VALUE IS INPUT THAT DOES NOT EXIST IN DB
		if form.user_id.data:
			player = Player.query.get(form.user_id.data)
			player_id = player.id 
		elif form.username.data:
		 	player = Player.query.filter(Player.name == form.username.data).first()
		 	player_id = player.id

		if player_id:
			matches = Match.query.filter(or_(Match.player1 == player_id, Match.player2 == player_id))
			player_total_matches = 0
			player_match_wins = 0
			player_match_draws = 0
			player_total_games = 0
			player_game_wins = 0
			for match in matches:
				player_total_matches += 1
				player_total_games += match.p1_game_wins
				player_total_games += match.p2_game_wins
				if match.p1_game_wins == match.p2_game_wins:
					player_match_draws += 1
				if match.player1 == player_id:
					player_game_wins += match.p1_game_wins
					if match.p1_game_wins > match.p2_game_wins:
						player_match_wins += 1
				if match.player2 == player_id:
					player_game_wins += match.p2_game_wins
					if match.p2_game_wins > match.p1_game_wins:
						player_match_wins += 1
			
			if player_total_matches > 0:
				player_data = {}
				player_data['match_wins'] = player_match_wins
				player_data['match_losses'] = player_total_matches - player_match_wins - \
					player_match_draws
				player_data['match_draws'] = player_match_draws
				player_data['match_win_rate'] = player_match_wins /\
				(player_total_matches - player_match_draws)
				player_data['game_wins'] = player_game_wins
				player_data['game_losses'] = player_total_games - player_game_wins
				player_data['game_win_rate'] = player_game_wins / player_total_games
			else:
				return 'no matches'

			return jsonify(player_data)
		else:
			return 'no such player'

	return render_template('statistics_page.html', form=form)