import os
from flask import Flask, jsonify, render_template, request, session, redirect
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit, send
from flask_socketio import join_room, leave_room
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
my_room = ""
my_rating = 500


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.cookies.get('username'):
        username = request.cookies.get('username')
        session[userID] = username
        print(username)
        global my_rating
        #my_rating = mongo.db.rating.find_one({'username': username})['rating']

        return render_template('wait_room.html', username=session[userID], room_log='')

    return redirect('http://localhost:5000/')



@socketio.on('join')
def on_join(data):
    print("XDXDXDXDXDDDXXD")
    username = session[userID]
    global my_room
    my_room = data['room']
    print("PLAYER", username, "JOINED ROOM", my_room)
    join_room(my_room)

    mongo.db.rooms.insert_one({
        "id": my_room,
        "rating": 500,
        "player": username
    })

    emit(username + ' has entered the room.', to=my_room)


@socketio.on('found')
def on_join(data):
    return render_template('game.html', username=session[userID], players=[session[userID], data['player']], room_id=my_room)


@socketio.on('leave')
def on_leave(data):
    username = session[userID]
    room = data['room']
    print("PLAYER", username, "LEFT ROOM", room)
    leave_room(room)
    mongo.db.rooms.deleteOne({"id": room})

    emit(username + ' has left the room.', to=room)

    if userID in session:
        print(session[userID] + " leaving")
        session.clear()
    return redirect('http://localhost:5000/logout')


@socketio.on('check_now')
def on_leave(data):
    rooms_raw = mongo.db.rooms.find()
    search_radius = data['range']

    for rooms in rooms_raw:
        rid = rooms['id']
        rating = rooms['rating']
        player = rooms['player']

        if player == session[userID]:
            continue

        print(rid, rating, player)

        if abs(rating - my_rating) <= search_radius:
            print("FOUND, WOAH!!!!")
            global my_room
            mongo.db.rooms.delete_one({"id": my_room})
            mongo.db.rooms.delete_one({"id": rid})
            leave_room(my_room)
            my_room = rid
            join_room(my_room)
            emit("found", {'player': session[userID], 'url': "http://localhost:5001/"}, to=my_room)

            #return render_template('game.html', username=session[userID], players=[session[userID], player], room_id=my_room)


@app.route('/room/leave')
def leave_game():
    if userID in session:
        print(session[userID] + " leaving")
        session.clear()
    return redirect('http://localhost:5000/logout')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5002)
