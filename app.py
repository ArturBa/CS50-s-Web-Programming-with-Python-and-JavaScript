import os

from flask import Flask, render_template, g, request
from flask_babel import Babel
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config.from_pyfile('app.config')
socketio = SocketIO(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/draw")
def mobile():
    return render_template('draw.html')


@socketio.on('connect')
def test_connect():
    print('Client connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
