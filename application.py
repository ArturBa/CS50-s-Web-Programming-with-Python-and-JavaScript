import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from model.chats import *
from model.messages import *
from model.users import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

users = Users()
messages = Messages()
chats = Chats()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/chat/<chat_id>')
def chat(chat_id):
    return render_template('chat.html', chats=chats.get(), msgs=messages.chat(chat_id))


@socketio.on("add user")
def create_user(data):
    users.add(data['username'])
    chats.add(data['username'], 'global')
    emit('user created', data)


@socketio.on("add msg")
def new_msg(data):
    messages.add(data['chat_id'], data['user_id'], data['msg'])
    msg = messages.chat(data['chat_id'])[-1]
    return_date = {'chat_id': data['chat_id'], 'msg': msg.msg, 'user': msg.user}
    emit('new msg', return_date)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
