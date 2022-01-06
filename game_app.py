import os
from flask import Flask, jsonify, render_template, request, session, redirect
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from game import attack, attack_success
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


@app.route('/', methods=['POST', 'GET'])
def index():
    print("key: " + APP_SECRET_KEY)
    
    if request.cookies.get('token'):
        token = request.cookies.get('token')
        payload = jwt.decode(token, APP_SECRET_KEY, ENC_ALGO)
        username = payload['username']
        session['username'] = username
        print("payload: {}".format(payload))
        return render_template('game.html', username=session['username'])

    return redirect('http://localhost:5000/')
    # if request.method == 'POST' and 'username' in request.form:
    #     username = request.form['username']
    #     return render_template('game.html', username=username)

    # return redirect('http://localhost:5000/')

    # # if 'username' in session:
    # #     return render_template('game.html', username=session['username'])
    # # return render_template('game.html', username=username)
    # return render_template('game.html', username=request.args.get('username'))

@app.route('/back')
def go_back():
    resp = redirect('http://localhost:5000/')
    if 'username' in session:
        resp.set_cookie('username', session['username'])

    return resp



@app.route('/game/leave')
def leave_game():
    resp = redirect('http://localhost:5000/logout')

    if 'username' in session:
        print(session['username'] + " leaving")
        log_out(resp, session)
    return resp


# @socketio.on('leave')
# def on_leave():
#     if 'username' in session:
        # session.pop('username')
        # session.clear()


@socketio.on('join_game')
def on_join(data):
    playername = data['data']

    print(playername + " joining")

    if 'username' in session:
        print("Player " + session['username'] + " already logged.")
    else:
        session['username'] = playername
        print("Player " + playername + " joined")

    print(request.sid)
    # players[request.sid] = playername


@socketio.on('attack')
def on_attack():
    print("Attack")
    print(request.sid)
    if 'username' in session:
        print(session['username'] + " attacked")
    emit('attack_response', {'data': attack_success(attack())})


@socketio.on('my_event')
def on_my_event(msg):
    print('my_event:\n' + msg['data'])
    emit('my_response', {'data': msg['data']})


@socketio.on('connect')
def on_connect():
    print('connect')
    if 'username' in session:
        print(session['username'] + " connected")
    emit('my_response', {'data': 'Connected'})


@socketio.on('disconnect')
def on_disconnect():
    print("client sid {} disconnected".format(request.sid))

    if 'username' in session:
        print("client session {} disconnected".format(session['username']))
    # print("client {} disconnected".format(players[request.sid]))


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app, host="0.0.0.0", port=5001)
    # app.run()