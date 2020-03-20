class Chat:
    def __init__(self, user_id, name):
        self.user_ids = []
        self.user_ids.append(user_id)
        self.name = name

    def add(self, user_id):
        self.user_ids.append(user_id)

    def users(self):
        return self.user_ids


class Chats:
    def __init__(self):
        self.chats = []

    def add(self, user_id, name):
        for chat in self.chats:
            if chat.name == name:
                chat.add(user_id)
                break
        else:
            self.chats.append(Chat(user_id, name))

    def remove_user(self, user_id, name):
        chat = self.get_chat(name)
        chat.user_ids.remove(user_id)
        if len(chat.user_ids) == 0:
            self.chats.remove(chat)

    def get_chat(self, name):
        for chat in self.chats:
            if name == chat.name:
                return chat

    def get(self):
        return self.chats


class ChatException(Exception):
    def __init__(self, message):
        """
        Constructor
        :param message: error message
        """
        super().__init__(message)
