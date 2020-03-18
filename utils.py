import hashlib
import os


def code_password(password):
    password += os.getenv('SALT')
    return hashlib.md5(password.encode()).hexdigest()
