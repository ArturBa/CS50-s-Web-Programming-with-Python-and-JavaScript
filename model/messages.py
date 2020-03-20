MAX_MESSAGE_LEN = 100


class Message:
    def __init__(self, timestamp, user, msg):
        self.timestamp = timestamp
        self.user = user
        self.msg = msg
