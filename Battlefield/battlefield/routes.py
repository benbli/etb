from flask import render_template, request, jsonify
from battlefield import app, db, bcrypt
from battlefield.models import Player

PLAYER_LIST = []

@app.route("/")
def hello():
	return "hello"



@app.route("/player", methods=['POST'])
def post_player():
	data = request.get_json()
	hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
	new_player = Player(first_name=data['first_name'], last_name=data['last_name'], password=hashed_password)
	db.session.add(new_player)
	db.session.commit()

	return ''



@app.route("/player", methods=['GET'])
def get_all_players():
	players = Player.query.all()

	output = []

	for player in players:
		player_data = {}
		player_data['id'] = player.id
		player_data['first_name'] = player.first_name
		player_data['last_name'] = player.last_name
		player_data['password'] = player.password
		player_data['time_created'] = player.time_created
		output.append(player_data)

	return jsonify({'users' : output})



@app.route("/player/<player_id>", methods=['GET'])
def get_player(player_id):
	player = Player.query.get(player_id)
	if player:
		player_data ={}
		player_data['id'] = player.id
		player_data['first_name'] = player.first_name
		player_data['last_name'] = player.last_name
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
		if data['first_name']:
			player.first_name = data['first_name']
		if data['last_name']:
			player.last_name = data['last_name']
		if data['password']:
			hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
			player.password = hashed_password
		db.session.commit()

		player_data ={}
		player_data['id'] = player.id
		player_data['first_name'] = player.first_name
		player_data['last_name'] = player.last_name
		player_data['password'] = player.password
		player_data['time_created'] = player.time_created

		return jsonify(player_data)
	else:
		return "player does not exist"