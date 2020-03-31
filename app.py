import os
import random

from flask import Flask, render_template, request, jsonify, g
from flask_babel import Babel
from flask_socketio import SocketIO

from animals import animals

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config.from_pyfile('app.config')
babel = Babel(app)
socket = SocketIO(app)

img = 0


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/mobile")
def mobile():
    return render_template('mobile.html', animal=random.choice(animals))


@app.route("/desktop")
def desktop():
    return render_template('desktop.html')


@app.route("/save_img", methods=['POST'])
def save_img():
    global img
    img = request.form.get('img64')
    socket.emit('new img')
    return jsonify({'status': 200})


@app.route('/get_img')
def get_img():
    response = {"img": img}
    return response


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
