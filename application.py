import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from model.chats import *
from model.users import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

users = Users()
chats = Chats()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/chat/<chat_id>')
def chat(chat_id):
    _chat = chats.get_chat(chat_id)
    if not _chat:
        return render_template('no-chat.html')
    return render_template('chat.html', chats=chats.get(), msgs=_chat.msg())


@socketio.on("add user")
def create_user(data):
    users.add(data['username'])
    chats.add(data['username'], 'global')
    emit('user created', data)


@socketio.on("add msg")
def new_msg(data):
    print(f"new msg: {data['msg']}")
    _chat = chats.get_chat(data['chat_id'])
    _chat.add_msg(user_id=data['chat_id'], msg=data['msg'])
    msg = chats.get_chat(data['chat_id']).msg()[-1]
    return_date = {'chat_id': data['chat_id'], 'msg': msg.msg, 'user': msg.user}
    emit('new msg', return_date)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
