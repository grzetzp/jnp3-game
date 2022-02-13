import os
from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from game import attack, attack_success
from config import APP_SECRET_KEY, MONGO_URI, ENC_ALGO, DEC_FORMAT
from login import LoginForm, RegisterForm, login_valid, log_out
from bson.json_util import dumps
import jwt
import bcrypt
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
app.config['MONGO_URI'] = MONGO_URI

mongo = PyMongo(app)

PLAYERS = ["p1", "p2"]


@app.route('/ping')
def ping_server():
    return "Server response." + str(app.config['SECRET_KEY']) + " " + app.config['MONGO_URI'] + "\n"


@app.route('/get_one')
def get_one():
    one = mongo.db.test_tb.find_one()

    return jsonify({"one": not not one})

@app.route('/get_all')
def get_all():
    all = mongo.db.test_tb.find()
    all_list = list(all)
    json_data = dumps(all_list)

    return json_data


@app.route('/put_one')
def put_one():
    mongo.db.test_tb.insert_one({
        "username": "testowy_" + random.choice(string.ascii_letters),
        "password": bcrypt.hashpw("testowe".encode(DEC_FORMAT), bcrypt.gensalt()),
    })

    return redirect(url_for('get_all'))

@app.route('/drop_all')
def drop():
    mongo.db.test_tb.drop()
    return redirect(url_for('get_all'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}".format(form.username.data))
        username = form.username.data
        password = form.password.data
        user = mongo.db.test_tb.find_one({'username': form.username.data})

        # TODO hashed password etc.
        if user is not None and login_valid(username, password, user):
            flash("User {} logged in.".format(form.username.data))

            session['username'] = username  # TODO jwt token
            return redirect(url_for('index', username=username))
        else:
            flash("Wrong username or password or smth")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Register requested for user {}".format(form.username.data))

        username = form.username.data
        password = form.password.data
        user = mongo.db.test_tb.find_one({'username': form.username.data})

        # TODO hashed password etc.
        if user is not None:
            flash("Username {} already exists. Pick different one".format(form.username.data))
            return redirect(url_for('register'))
        else:
            flash("Registered.")
            mongo.db.test_tb.insert_one({
                "username": username,
                "password": bcrypt.hashpw(password.encode(DEC_FORMAT), bcrypt.gensalt()),
            })
            session['username'] = username
            return redirect(url_for('index', username=username))
    return render_template('register.html', form=form)


@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        flash("from session")
        return render_template('index.html', username=session['username'])

    if request.cookies.get('username'):
        flash("from cookies")
        username = request.cookies.get('username')
        session['username'] = username
        return render_template('index.html', username=session['username'])

    return render_template('index.html')


@app.route('/redirect')
def do_redirect():
    return redirect('http://localhost:5001?username=testowy')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    resp = redirect(url_for('index'))
    log_out(resp, session)
    return resp


@app.route('/game', methods=['POST', 'GET'])
def play_game():
    if 'username' in session:
        PLAYERS.append(session['username'])
        resp = redirect('http://localhost:5002/', code=307)

        print("key: " + APP_SECRET_KEY)
        token = jwt.encode({
            'username': session['username'],
            'room': 0,
            }, APP_SECRET_KEY)

        resp.set_cookie('token', token)
        resp.set_cookie('username', session['username'])

        return resp

    return redirect(url_for('index'))


@app.route('/users')
def get_users():
    users_raw = mongo.db.test_tb.find()

    if not users_raw:
        return "Database error"

    users = [{"id": user['id'], "username": user['username']} for user in users_raw]
    return jsonify({"all_users": users})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
