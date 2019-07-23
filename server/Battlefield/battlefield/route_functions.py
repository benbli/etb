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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_player = Player(name=form.username.data, password=hashed_password)
        db.session.add(new_player)
        db.session.commit()

        return redirect(url_for('get_all_players'))
    return render_template('register.html', form=form)


@app.route("/create_tournament", methods=['GET', 'POST'])
def create_tournament():

    form = TournamentForm()
    dbplayers = Player.query.all()
    playerIds = request.form.getlist('checked')

    # WHEN SUBMITTED, ADDS NEW ENTRY TO TOURNAMENTS DB
    # ADDS NEW ENTRY TO SCOREBORAD DB PER PLAYER
    if form.validate_on_submit():
        new_tournament = Tournament(name=form.name.data)
        db.session.add(new_tournament)
        players = Player.query.filter(Player.id.in_(playerIds)).all()

        for player in players:
            new_scoreboard = Scoreboard(
                player=player.id, tournamentId=new_tournament.id)
            db.session.add(new_scoreboard)
        db.session.commit()

        # NOT CERTAIN IF SESSION IS SECURE
        session['tournamentId'] = new_tournament.id

        return redirect(url_for('seating'))

    return render_template('create_tournament.html', form=form, dbplayers=dbplayers)


@app.route("/seating", methods=['GET', 'POST'])
def seating():

    form = SeatingForm()
    # BELOW THE CHANGE OF THE TOURNAMENT ID IS JUST FOR TESTING PURPOSES
    tournamentId = session.get('tournamentId')
    # tournamentId = 200

    ##################################################
    # GENERATE LIST OF PLAYERS SORTED BY MOST POINTS #
    ##################################################
    scoreboard_dict = {}       # DICT KEY: PLAYER ID; VALUE: POINTS
    player_id_list = []        # LIST OF PLAYER IDs
    max_points = 0             # GREATEST POINTS VALUE AMONG PLAYERS
    # LIST OF LISTS, WHERE EACH SUBLIST CONTAINS ALL PLAYERS OF A CERTAIN POINT VALUE. SOME SUBLISTS MIGHT BE EMPTY.
    points_lists = []
    # A SINGLE LIST OF ALL THE ELEMENTS FROM SUBLISTS IN points_lists. MAINTAINS ORDER BY POINT VALUE. NOTE THAT THIS IS A LIST OF PLAYER IDs, NOT A LIST OF LISTS.
    points_combined_list = []
    # DICT KEY: PLAYER ID; VALUE: PLAYER NAME. THIS IS FOR FRONT END PURPOSES
    player_dict = {}
    name_list = []             # LIST OF PLAYER NAMES. THIS IS FOR FRONT END PURPOSES

    # PULLS THE SCOREBORADS BY TOURNAMENT ID
    scoreboards = Scoreboard.query.filter(
        Scoreboard.tournamentId == tournamentId)

    # GRAB SCOREBOARD OF EACH PARTICIPANT IN TOURNAMENT AND CALCULATE THEIR POINTS
    # player_id_list POPULATED (UNSORTED)
    # max_points IS SET
    for scoreboard in scoreboards:
        points = (scoreboard.wins * 3) + (scoreboard.draws * 1)
        scoreboard_dict.update({scoreboard.player: points})
        player_id_list.append(scoreboard.player)
        if points > max_points:
            max_points = points

    # PULLS PLAYERS THAT ONLY IN player_id_list
    players = Player.query.filter(Player.id.in_(player_id_list)).all()

    # GENERATE LISTS, WHERE EACH LIST CONTAINS ALL PLAYERS WITH A SPECIFIC POINT VALUE. EACH LIST IS SHUFFLED THEN APPENDED TO points_lists
    temp_max_points = max_points
    while temp_max_points >= 0:
        these_points = []
        for key, value in scoreboard_dict.items():
            if value == temp_max_points:
                these_points.append(key)
        random.shuffle(these_points)
        points_lists.append(these_points)
        temp_max_points -= 1

    # POPULATES points_combined_list USING points_lists
    for this_list in points_lists:
        for i in this_list:
            points_combined_list.append(i)

    # POPULATES player_dict
    for player in players:
        player_dict.update({player.id: player.name})

    # POPULATES name_list USING player_dict
    for i in points_combined_list:
        name_list.append(player_dict[i])

    # CURRENTLY DOES NOT CHECK for EMPTY NAME or NUMBERS of PLAYERS
    if form.is_submitted():
        round_number = request.form.get()
        matches = Match.query.filter(Match.tournamentId == tournamentId)

        # A LIST OF LISTS, WHERE EACH SUBLIST CONTAINS THE PLAYERS THAT WOULD BE PAIRED UP.
        matchup_list = []
        # A LIST OF PLAYER NAME FOR EACH MATCHUP. FOR FRONT END PURPOSES.
        matchup_list_names = []

    # IF THE LAST PAIR IS A CONFLICT BUT EVERY OTHER PIARS IS OKAY THIS ALGORITHM WON'T WORK. WE'll ALSO HIT AN ERROR
    # COMMENT BELOW ALGORITHM SINCE ABOVEMENTIONED ISSUE. WILL FIX THIS LATER ON.
        # for i in range(len(points_combined_list)):
        #     if (i % 2 == 0) and (len(points_combined_list) - 1 > i):
        #         counter = 2
        #         for match in matches:
        #             if points_combined_list[i] == match.player1:
        #                 if points_combined_list[i + 1] == match.player2:
        #                     temp_player = points_combined_list[i + 1]
        #                     points_combined_list[i + 1] = points_combined_list[i + counter]
        #                     points_combined_list[i + counter] = temp_player
        #                     counter += 1

        #             elif points_combined_list[i] == match.player2:
        #                 if points_combined_list[i + 1] == match.player1:
        #                     temp_player = points_combined_list[i + 1]
        #                     points_combined_list[i + 1] = points_combined_list[i + counter]
        #                     points_combined_list[i + counter] = temp_player
        #                     counter += 1

        # POPULATES matchup_list by using points_combined_list. WHEN NUMBERS OF PLAYERS IS ODD, THE LAST PLAYER WILL PAIR WITH PLAYER ID 0 WHO DOESN'T EXIST IN THE DB, EFFECTIVELY GIVING THE LAST PLAYER A BYE.
        for player in points_combined_list:
            if points_combined_list.index(player) % 2 == 0:
                matchup = []
                matchup.append(
                    points_combined_list[points_combined_list.index(player)])
                if len(points_combined_list) - points_combined_list.index(player) == 1:
                    matchup.append(0)
                else:
                    matchup.append(
                        points_combined_list[points_combined_list.index(player) + 1])
                matchup_list.append(matchup)

        # COMMIT MATCH ENTRIES TO DB
        for matchup in matchup_list:
            new_match = Match(
                player1=matchup[0], player2=matchup[1],
                p1_game_wins=0, p2_game_wins=0,
                tournamentId=tournamentId
            )
            db.session.add(new_match)
        db.session.commit()

        # POPULATES matchup_list_names by matchup_names
        for matchup in matchup_list:
            matchup_names = []
            for player in matchup:
                if player != 0:
                    matchup_names.append(player_dict[player])
                else:
                    matchup_names.append('BYE')
            matchup_list_names.append(matchup_names)

        return render_template('seating.html', player_list = matchup_list_names, round_number = round_number, form=form)

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
            player = Player.query.filter(
                Player.name == form.username.data).first()
            player_id = player.id

        if player_id:
            matches = Match.query.filter(
                or_(Match.player1 == player_id, Match.player2 == player_id))
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
                player_data['game_losses'] = player_total_games - \
                    player_game_wins
                player_data['game_win_rate'] = player_game_wins / \
                    player_total_games
            else:
                return 'no matches'

            return jsonify(player_data)
        else:
            return 'no such player'

    return render_template('statistics_page.html', form=form)


@app.route("/standings/<tournament_id>", methods=['GET'])
def standings(tournament_id):
    tournament = Tournament.query.get(tournament_id)
    scoreboards = Scoreboard.query.filter(
        Scoreboard.tournamentId == tournament_id)

    player_points_dict = {}
    for scoreboard in scoreboards:
        points = (scoreboard.wins * 3) + (scoreboard.draws * 1)
        player_points_dict.update(
            {scoreboard.player: [points, scoreboard.tiebreak]})

    max_points = 0
    players_points_list = []

    for key in player_points_dict:
        player_points = player_points_dict[key][0]
        if max_points < player_points:
            max_points = player_points

    temp_max_points = max_points
    while temp_max_points >= 0:
        points_group = []
        for key in player_points_dict:
            player_points = player_points_dict[key]
            if player_points == temp_max_points:
                points_group.append(key)

        no_swap = False
        while no_swap == False:
            no_swap = True
            for player in points_group:
                i = points_group.index(player)
                if i < len(points_group) - 1:
                    if points_group[i][1] < points_group[i + 1][1]:
                        temp_points_group[i] = points_group[i]
                        points_group[i] = points_group[i + 1]
                        points_group[i + 1] = temp_points_group[i]
                        no_swap = False
        player_points_list.append(points_group)
        # NEED TO CONVERT player_points_list, FROM LIST OF LISTS INTO A LIST OF INDIVIDUAL "PLAYER ID"

        temp_max_points -= 1

    return '123'
    # players_points_list.append(points_group)
