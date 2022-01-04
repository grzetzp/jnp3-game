import os
from flask import Flask, jsonify, render_template, request, session, redirect
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from game import attack, attack_success


MONGO_URI = 'mongodb://test_mongodb:27017/test_mongodb'
# MONGO_HOSTNAME = os.environ[]

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['MONGO_URI'] = MONGO_URI

mongo = PyMongo(app)
socketio = SocketIO(app, manage_session=False)

userID = 'playername'
players = ["p1", "p2"]

@app.route('/ping')
def ping_server():
    return "Server response.\n"


@app.route('/get_one')
def get_one():
    one = mongo.db.test_tb.find_one()

    return jsonify({"one": not not one})


@app.route('/api/put_one/<id>')
def put_one(id: int):
    mongo.db.test_tb.insert_one({
            "id": int(id),
            "name": "testowy_" + id
            })

    return "One put"

# @app.route('/')
# def home_page():

#     return "Success. Welcome."
@app.route('/', methods=['POST', 'GET'])
def index():
    if userID in session:
        return render_template('index.html', username=session[userID])
    return render_template('index.html')


@app.route('/redirect')
def do_redirect():
    return redirect('http://localhost:5001/')    


@app.route('/game', methods=['POST', 'GET'])
def play_game():
    print("game")
    if request.method == 'POST' and 'username' in request.form:
        if userID in session:
            print("player " + session[userID] + " already logged")
        else:
            username = request.form['username']
            session[userID] = username
            print("player " + session[userID] + " joined")
            print(username + " joined")
    if userID in session:
        players.append(session[userID])
        return render_template('game.html', username=session[userID], players=players)
    return render_template('index.html')



@app.route('/game/leave')
def leave_game():
    if userID in session:
        print(session[userID] + " leaving")
        # session.pop(userID)
        session.clear()
    return render_template('index.html')


# @socketio.on('leave')
# def on_leave():
#     if userID in session:
        # session.pop(userID)
        # session.clear()


@socketio.on('join_game')
def on_join(data):
    playername = data['data']

    print(playername + " joining")

    if userID in session:
        print("Player " + session[userID] + " already logged.")
    else:
        session[userID] = playername
        print("Player " + playername + " joined")

    print(request.sid)
    # players[request.sid] = playername


@socketio.on('attack')
def on_attack():
    print("Attack")
    print(request.sid)
    if userID in session:
        print(session[userID] + " attacked")
    emit('attack_response', {'data': attack_success(attack())})


@socketio.on('my_event')
def on_my_event(msg):
    print('my_event:\n' + msg['data'])
    emit('my_response', {'data': msg['data']})


@socketio.on('connect')
def on_connect():
    print('connect')
    if userID in session:
        print(session[userID] + " connected")
    emit('my_response', {'data': 'Connected'})


@socketio.on('disconnect')
def on_disconnect():
    print("client sid {} disconnected".format(request.sid))

    if userID in session:
        print("client session {} disconnected".format(session[userID]))
    # print("client {} disconnected".format(players[request.sid]))


@app.route('/users')
def get_users():
    users_raw = mongo.db.test_tb.find()

    if not users_raw:
        return "Database error"

    users = [{"id": user['id'], "name": user['name']} for user in users_raw]
    return jsonify({"all_users": users})

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app, host="0.0.0.0", port=5000)
    # app.run()