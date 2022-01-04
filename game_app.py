import os
from flask import Flask, jsonify, render_template, request, session, redirect
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from game import attack, attack_success
from config import APP_SECRET_KEY, MONGO_URI


# MONGO_URI = 'mongodb://test_mongodb:27017/test_mongodb'
# MONGO_HOSTNAME = os.environ[]

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['MONGO_URI'] = MONGO_URI

mongo = PyMongo(app)
socketio = SocketIO(app, manage_session=False)

userID = 'username'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.cookies.get('username'):
        username = request.cookies.get('username')
        session[userID] = username
        print(username)
        return render_template('game.html', username=session[userID])

    return redirect('http://localhost:5000/')
    # if request.method == 'POST' and 'username' in request.form:
    #     username = request.form['username']
    #     return render_template('game.html', username=username)

    # return redirect('http://localhost:5000/')

    # # if userID in session:
    # #     return render_template('game.html', username=session[userID])
    # # return render_template('game.html', username=username)
    # return render_template('game.html', username=request.args.get('username'))

@app.route('/back')
def go_back():
    resp = redirect('http://localhost:5000/')
    resp.set_cookie(userID, session[userID])

    return resp



@app.route('/game/leave')
def leave_game():
    if userID in session:
        print(session[userID] + " leaving")
        # session.pop(userID)
        session.clear()
    return redirect('http://localhost:5000/logout')
    # return render_template('index.html')


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


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app, host="0.0.0.0", port=5001)
    # app.run()