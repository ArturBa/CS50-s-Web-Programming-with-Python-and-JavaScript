import os

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_socketio import SocketIO, emit

from model.chats import *
from model.users import *

app = Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
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
    return render_template('chat.html', msgs=_chat.msg())


@app.route('/new/')
def new_chat():
    return render_template('new-chat.html', chat_name=None)


@app.route('/new_chat/', methods=['POST'])
def new_chat_create():
    if request.method != 'POST':
        flash(f'Wrong method user. {request.method} is not POST')
        return redirect(url_for('new_chat'))

    for _chat in chats.get():
        if _chat.name == request.form.get('chat_name'):
            flash(f'Chat with this name already exists. Try something else')
            return redirect(url_for('new_chat'))
    try:
        chats.add_user(request.form.get('user_id'), request.form.get('chat_name'))
        return redirect(url_for('chat', chat_id=request.form.get('chat_name')))
    except Exception as exception:
        print(exception)
        return redirect(url_for('new_chat'))


@app.route('/all_chats')
def all_chats():
    return render_template("chats.html", chats=chats.get())


@socketio.on("add user")
def create_user(data):
    users.add(data['username'])
    chats.add_user(data['username'], 'global')
    emit('user created', data)


@socketio.on("add msg")
def new_msg(data):
    _chat = chats.get_chat(data['chat_id'])
    _chat.add_msg(user_id=data['user_id'], msg=data['msg'])
    msg = chats.get_chat(data['chat_id']).msg()[-1]
    return_date = {'chat_id': data['chat_id'], 'msg': msg.msg, 'user': msg.user,
                   'timestamp': msg.timestamp.strftime("%H:%M:%S")}
    emit('new msg', return_date)


@socketio.on('get chats')
def get_chats(data):
    ret_chats = []
    for _chat in chats.get_user(data['user_id']):
        ret_chats.append(_chat.name)
    _chats = {'chats': ret_chats}
    emit('user chats', _chats)


@socketio.on('add user to chat')
def add_user_to_chat(data):
    chats.add_user(data['user_id'], data['chat_id'])
    emit('user added to chat', data)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
