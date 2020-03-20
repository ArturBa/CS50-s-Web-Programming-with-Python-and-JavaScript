class User:
    def __init__(self, name):
        self.name = name


class Users:
    def __init__(self):
        self.users = []

    def add(self, name):
        for user in self.users:
            if name == user.name:
                raise UsersException(f"Username: {name} already taken")
        self.users.append(User(name=name))


class UsersException(Exception):

    def __init__(self, message):
        """
        Constructor
        :param message: error message
        """
        super().__init__(message)
