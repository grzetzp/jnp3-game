import os
from flask import Flask, jsonify, render_template, request, session
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


@app.route('/', methods=['POST', 'GET'])
def index():
    if userID in session:
        return render_template('game_test.html', username=session[userID])
    return render_template('game_test.html')


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    socketio.run(app, host="0.0.0.0", port=5001)
    # app.run()