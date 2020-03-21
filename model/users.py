class User:
    """
    Class for containing all user info
    """

    def __init__(self, name):
        """
        User init
        :param name: user name
        """
        self.name = name


class Users:
    """
    Class for handling all users
    """

    def __init__(self):
        """
        Init
        """
        self.users = []

    def add(self, name):
        """
        Add a user
        :param name: user name
        :raise: if username already exits
        """
        for user in self.users:
            if name == user.name:
                break
        else:
            self.users.append(User(name=name))


class UsersException(Exception):
    """
    Class for user exception
    """

    def __init__(self, message):
        """
        Constructor
        :param message: error message
        """
        super().__init__(message)
