from flask import render_template, request, jsonify, redirect, url_for, session
from battlefield import app, db, bcrypt
from battlefield.models import Player, Scoreboard, Match, Tournament
from battlefield.forms import TournamentForm, RegisterForm, StatisticsForm, SeatingForm
from sqlalchemy import or_
import random


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
        # db.session.commit()

        players = Player.query.filter(Player.id <= numofplayers)
        # player_list = {}
        for player in players:
            new_scoreboard = Scoreboard(player=player.id, tournamentId=new_tournament.id)
            db.session.add(new_scoreboard)
        db.session.commit()
        #     player_list.update({player.id: player.name})
        # session['player_list'] = player_list
        session['tournamentId'] = new_tournament.id

        return redirect(url_for('seating'))

    return render_template('create_tournament.html', form=form)


@app.route("/seating", methods=['GET', 'POST'])
def seating():

    form = SeatingForm()
    # tournamentId = session.get('tournamentId')
    tournamentId = 200
    scoreboards = Scoreboard.query.filter(Scoreboard.tournamentId == tournamentId)

    scoreboard_dict = {}
    player_id_list = []
    max_points = 0
    for scoreboard in scoreboards:
        points = (scoreboard.wins * 3) + (scoreboard.draws * 1)
        scoreboard_dict.update({scoreboard.player: points})
        player_id_list.append(scoreboard.player)
        if points > max_points:
            max_points = points

    points_lists = []
    while max_points >= 0:
        these_points = []
        for key, value in scoreboard_dict.items():
            if value == max_points:
                these_points.append(key)
        random.shuffle(these_points)
        points_lists.append(these_points)
        max_points -= 1

    points_combined_list = []
    for this_list in points_lists:
        for i in this_list:
            points_combined_list.append(i)

    players = Player.query.filter(Player.id.in_(player_id_list)).all()

    player_dict = {}
    for player in players:
        player_dict.update({player.id: player.name})

    # key_list = []
    # for key in player_dict:
    #     key_list.append(key)

    name_list = []
    for i in points_combined_list:
        name_list.append(player_dict[i])

    # CURRENTLY DOES NOT CHECK for EMPTY NAME or NUMBERS of PLAYERS
    if form.is_submitted():
        matches = Match.query.filter(Match.tournamentId == tournamentId)
    # IF THE LAST PAIR IS A CONFLICT BUT EVERY OTHER PIARS IS OKAY THIS ALGORITHM WON'T WORK. WE'll ALSO HIT AN ERROR
        for i in range(len(points_combined_list)):
            if (i % 2 == 0) and (len(points_combined_list) - 1 > i):
                counter = 2
                for match in matches:
                    if points_combined_list[i] == match.player1:
                        if points_combined_list[i + 1] == match.player2:
                            temp_player = points_combined_list[i + 1]
                            points_combined_list[i + 1] = points_combined_list[i + counter]
                            points_combined_list[i + counter] = temp_player
                            counter += 1

                    elif points_combined_list[i] == match.player2:
                        if points_combined_list[i + 1] == match.player1:
                            temp_player = points_combined_list[i + 1]
                            points_combined_list[i + 1] = points_combined_list[i + counter]
                            points_combined_list[i + counter] = temp_player
                            counter += 1

        matchup_list = []
        for player in points_combined_list:
            if points_combined_list.index(player) % 2 == 0:
                matchup = []
                matchup.append(points_combined_list[points_combined_list.index(player)])
                if len(points_combined_list) - points_combined_list.index(player) == 1:
                    matchup.append(0)
                else:
                    matchup.append(points_combined_list[points_combined_list.index(player) + 1])
                matchup_list.append(matchup)

        for matchup in matchup_list:
            new_match = Match(
                player1=matchup[0], player2=matchup[1],
                p1_game_wins=0, p2_game_wins=0,
                tournamentId=tournamentId
            )
        #     db.session.add(new_match)
        # db.session.commit()

        matchup_list_names = []

        for matchup in matchup_list:
            matchup_names = []
            for player in matchup:
                if player != 0:
                    matchup_names.append(player_dict[player])
                else:
                    matchup_names.append('BYE')
            matchup_list_names.append(matchup_names)

        return jsonify(matchup_list_names)

    return render_template('seating.html', player_list=name_list, form=form)


@app.route("/view_stats", methods=['GET', 'POST'])
def view_stats():
    form = StatisticsForm()
    if form.is_submitted():
        player_id = 0

        # FIX WHEN VALUE IS INPUT THAT DOES NOT EXIST IN DB
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
