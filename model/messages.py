import datetime
MAX_MESSAGE_LEN = 100


class Message:
    """
    Class for a message
    """

    def __init__(self, user, msg, timestamp=datetime.datetime.now()):
        """
        Init a new message
        :param user: message owner
        :param msg: message text
        :param timestamp: message time
        """
        self.timestamp = timestamp
        self.user = user
        self.msg = msg
