from .messages import Message, MAX_MESSAGE_LEN


class Chat:
    """
    Class for a single chat
    """

    def __init__(self, user_id, name):
        """
        Initialize function
        :param user_id: first user id
        :param name: chat name
        """
        self.user_ids = []
        self.user_ids.append(user_id)
        self.name = name
        self.messages = []

    def add_user(self, user_id):
        """
        Add user to a chat
        :param user_id: user to add
        """
        self.user_ids.append(user_id)

    def users(self):
        """
        Get users in a chat
        :return: users ids
        """
        return self.user_ids

    def msg(self):
        """
        Get chat messages
        :return: chat messages
        """
        return self.messages

    def add_msg(self, user_id, msg):
        """
        Add message into chat
        :param user_id: message author
        :param msg: message
        """
        if len(self.messages) == MAX_MESSAGE_LEN:
            self.messages.pop(0)
        self.messages.append(Message(datetime.datetime.now(), user=user_id, msg=msg))


class Chats:
    """
    Class for all chats
    """

    def __init__(self):
        """
        Initial function
        """
        self.chats = []

    def add_user(self, user_id, name):
        """
        Add a user to a chat
        :param user_id: user to add
        :param name: chat name
        """
        for chat in self.chats:
            if chat.name == name:
                chat.add_user(user_id)
                break
        else:
            self.chats.append(Chat(user_id, name))

    def remove_user(self, user_id, name):
        """
        Remove user from a chat
        :param user_id: user to remove
        :param name: chat name
        """
        chat = self.get_chat(name)
        chat.user_ids.remove(user_id)
        if len(chat.user_ids) == 0:
            self.chats.remove(chat)

    def get_chat(self, name):
        """
        Get chat
        :param name: chat name
        :return: chat
        """
        for chat in self.chats:
            if name == chat.name:
                return chat

    def get(self):
        """
        Get all chats list
        :return: chats list
        """
        return self.chats


class ChatException(Exception):
    def __init__(self, message):
        """
        Constructor
        :param message: error message
        """
        super().__init__(message)
