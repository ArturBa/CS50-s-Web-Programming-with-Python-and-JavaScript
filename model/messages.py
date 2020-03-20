import datetime

MAX_MESSAGE_LEN = 100


class Message:
    def __init__(self, chat_id, timestamp, user, msg):
        self.chat_id = chat_id
        self.timestamp = timestamp
        self.user = user
        self.msg = msg


class Messages:
    def __init__(self):
        self.messages = []

    def add(self, chat_id, user, msg):
        if len(self.messages) == MAX_MESSAGE_LEN:
            self.messages.pop(0)
        self.messages.append(Message(chat_id=chat_id, timestamp=datetime.datetime.now(), user=user, msg=msg))

    def chat(self, chat_id):
        return_msg = []
        for msg in self.messages:
            if msg.chat_id == chat_id:
                return_msg.append(msg)

        return return_msg
