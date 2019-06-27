from flask import render_template, request, jsonify, redirect, url_for
from battlefield import app, db, bcrypt
from battlefield.models import Player, Scoreboard, Match, Tournament
from battlefield.forms import TournamentForm, RegisterForm


@app.route("/")
def hello():
    return "main page"


######################
#######PLAYER#########
######################

@app.route("/player", methods=['POST'])
def post_player():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_player = Player(name=data['name'], password=hashed_password)
    db.session.add(new_player)
    db.session.commit()

    return ''


@app.route("/player", methods=['GET'])
def get_all_players():
    players = Player.query.all()

    output = []
    if players:
        for player in players:
            player_data = {}
            player_data['id'] = player.id
            player_data['name'] = player.name
            player_data['password'] = player.password
            player_data['time_created'] = player.time_created
            output.append(player_data)

        return jsonify({'players': output})
    else:
        return "no players"


@app.route("/player/<player_id>", methods=['GET'])
def get_player(player_id):
    player = Player.query.get(player_id)

    if player:
        player_data = {}
        player_data['id'] = player.id
        player_data['name'] = player.name
        player_data['password'] = player.password
        player_data['time_created'] = player.time_created

        return jsonify(player_data)
    else:
        return "player does not exist"


@app.route("/player/<player_id>", methods=['PUT'])
def update_player(player_id):
    player = Player.query.get(player_id)

    if player:
        data = request.get_json()
        # Hits an error if only one, the other, or neither are updated
        if data['name']:
            player.name = data['name']
        if data['password']:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            player.password = hashed_password

        db.session.commit()

        player_data = {}
        player_data['id'] = player.id
        player_data['name'] = player.name
        player_data['password'] = player.password
        player_data['time_created'] = player.time_created

        return jsonify(player_data)
    else:
        return "player does not exist"

######################
#######Tournament#####
######################


@app.route("/tournament", methods=['POST'])
def post_tournament():
    data = request.get_json()
    new_tournament = Tournament(name=data['name'])
    db.session.add(new_tournament)
    db.session.commit()

    return ''


@app.route("/tournament", methods=['GET'])
def get_all_tournament():
    tournaments = Tournament.query.all()

    output = []
    if tournaments:
        for tournament in tournaments:
            tournament_data = {}
            tournament_data['id'] = tournament.id
            tournament_data['name'] = tournament.name
            output.append(tournament_data)

        return jsonify({'tournament': output})
    else:
        return "tournament does not exist"


@app.route("/tournament/<tournament_id>", methods=['GET'])
def get_tournament(tournament_id):
    tournament = Tournament.query.get(tournament_id)

    if tournament:
        tournament_data = {}
        tournament_data['id'] = tournament.id
        tournament_data['name'] = tournament.name
        return jsonify(tournament_data)
    else:
        return "tournament does not exist"


@app.route("/tournament/<tournament_id>", methods=['PUT'])
def update_tournament(tournament_id):
    tournament = Tournament.query.get(tournament_id)

    if tournament:
        data = request.get_json()
        # Hits an error if only one, the other, or neither are updated
        if data['name']:
            tournament.name = data['name']

        db.session.commit()

        tournament_data = {}
        tournament_data['id'] = tournament.id
        tournament_data['name'] = tournament.name

        return jsonify(tournament_data)
    else:
        return "tournament does not exist"


######################
#######Socoreboard####
######################


@app.route("/scoreboard", methods=['POST'])
def post_scoreboard():
    data = request.get_json()
    # tiebreak_scores =  !!!!!!!!!NEED TO COME UP WITH THE FORMULA LATER!!!!!!!!!
    new_scoreboard = Scoreboard(

        # So here player is equivalent to name?
        player=data['player_name'], wins=data['win'],
        losses=data['loss'], draws=data['draw'],
        # tiebreak=tiebreak_scores,
        tiebreak=data['tiebreakscores'],
        tournamentId=data['tournamentId']

    )

    db.session.add(new_scoreboard)
    db.session.commit()
    return ''


@app.route("/scoreboard", methods=['GET'])
def get_all_scoreboards():
    scoreboards = Scoreboard.query.all()

    output = []
    if scoreboards:
        for scoreboard in scoreboards:
            scoreboard_data = {}
            scoreboard_data['id'] = scoreboard.id
            scoreboard_data['player_name'] = scoreboard.player
            scoreboard_data['win'] = scoreboard.wins
            scoreboard_data['loss'] = scoreboard.losses
            scoreboard_data['draw'] = scoreboard.draws
            scoreboard_data['tiebreakscores'] = scoreboard.tiebreak
            scoreboard_data['tournamentId'] = scoreboard.tournamentId
            output.append(scoreboard_data)

        return jsonify({'scoreboards': output})

    else:
        return "no scoreboards"


@app.route("/scoreboard/<scoreboard_id>", methods=['GET'])
def get_scoreboard(scoreboard_id):
    scoreboard = Scoreboard.query.get(scoreboard_id)

    if scoreboard:
        scoreboard_data = {}
        scoreboard_data['id'] = scoreboard.id
        scoreboard_data['player_name'] = scoreboard.player
        scoreboard_data['win'] = scoreboard.wins
        scoreboard_data['loss'] = scoreboard.losses
        scoreboard_data['draw'] = scoreboard.draws
        scoreboard_data['tiebreakscores'] = scoreboard.tiebreak
        scoreboard_data['tournamentId'] = scoreboard.tournamentId

        return jsonify(scoreboard_data)


######################
#######MATCHES########
######################

@app.route("/match", methods=['POST'])
def post_match():
    data = request.get_json()
    new_match = Match(player1=data['player1'], player2=data['player2'], p1_game_wins=data['p1_game_wins'], p2_game_wins=data['p2_game_wins'], tournamentId=data['tournamentId'])
    db.session.add(new_match)
    db.session.commit()

    return ''


@app.route("/match", methods=['GET'])
def get_all_matches():
    matches = Match.query.all()

    output = []
    if matches:
        for match in matches:
            match_data = {}
            match_data['player1'] = match.player1
            match_data['player2'] = match.player2
            match_data['p1_game_wins'] = match.p1_game_wins
            match_data['p2_game_wins'] = match.p2_game_wins
            match_data['tournamentId'] = match.tournamentId
            output.append(match_data)

        return jsonify({'matches': output})
    else:
        return "no matches"