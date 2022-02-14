import os
from flask import Flask, jsonify, render_template, request, session, redirect
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit, join_room
from game import attack_success
from config import APP_SECRET_KEY, MONGO_URI, ENC_ALGO, DEC_FORMAT
from login import log_out
import jwt

# MONGO_URI = 'mongodb://test_mongodb:27017/test_mongodb'
# MONGO_HOSTNAME = os.environ[]

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['MONGO_URI'] = MONGO_URI

mongo = PyMongo(app)
socketio = SocketIO(app, manage_session=False)

my_room = ""


@app.route('/', methods=['POST', 'GET'])
def index():
    print("key: " + APP_SECRET_KEY)

    if request.cookies.get('token'):
        token = request.cookies.get('token')
        payload = jwt.decode(token, APP_SECRET_KEY, ENC_ALGO)
        username = payload['username']
        session['username'] = username
        print("payload: {}".format(payload))
        global my_room
        my_room = request.cookies.get('room')

        return render_template('game.html', username=session['username'], room=my_room)

    return redirect('http://localhost:5000/')


@app.route('/back', methods=['POST', 'GET'])
def go_back():
    resp = redirect('http://localhost:5000/')
    if 'username' in session:
        resp.set_cookie('username', session['username'])

    return resp


@socketio.on('join_game')
def on_join():
    join_room(my_room)


@socketio.on('win')
def on_join():
    my_rating = mongo.db.rating.find_one({'username': session['username']})['rating']
    mongo.db.rating.delete_one({"username": session['username'], 'rating': my_rating})
    my_rating += 10
    mongo.db.rating.insert_one({"username": session['username'], 'rating': my_rating})


@socketio.on('lose')
def on_join():
    my_rating = mongo.db.rating.find_one({'username': session['username']})['rating']
    mongo.db.rating.delete_one({"username": session['username'], 'rating': my_rating})
    my_rating -= 10
    mongo.db.rating.insert_one({"username": session['username'], 'rating': my_rating})


@socketio.on('tie')
def on_join():
    my_rating = mongo.db.rating.find_one({'username': session['username']})['rating']
    mongo.db.rating.delete_one({"username": session['username'], 'rating': my_rating})
    my_rating += 1
    mongo.db.rating.insert_one({"username": session['username'], 'rating': my_rating})


attack_success_chance = 0.5


@socketio.on('train')
def on_attack():
    global attack_success_chance
    attack_success_chance += 0.01
    attack_success_chance = min(attack_success_chance, 1)
    emit('train_response', {'data': attack_success_chance, 'player': session['username']}, to=my_room)


@socketio.on('attack')
def on_attack():
    print("Attack")
    print(my_room)
    if 'username' in session:
        print(session['username'] + " attacked")
    emit('attack_response', {'data': attack_success(attack_success_chance), 'player': session['username']}, to=my_room)


@socketio.on('my_event')
def on_my_event(msg):
    print('my_event:\n' + msg['data'])
    emit('my_response', {'data': msg['data']}, to=my_room)


@socketio.on('connect')
def on_connect():
    print('connect')
    if 'username' in session:
        print(session['username'] + " connected")
    emit('my_response', {'data': 'Connected'}, to=my_room)


@socketio.on('disconnect')
def on_disconnect():
    print("client sid {} disconnected".format(request.sid))

    if 'username' in session:
        print("client session {} disconnected".format(session['username']))


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app, host="0.0.0.0", port=5001)
    # app.run()
