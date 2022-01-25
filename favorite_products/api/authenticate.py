import logging

from functools import wraps

from flask_restx import abort


def basic_authentication():
    logging.info('basic_authentication executado com sucesso')
    return True


def basic_authorization():
    logging.info('basic_authorization executado com sucesso')


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        acct = basic_authentication()
        if acct:
            basic_authorization()
            return func(*args, **kwargs)
        abort(401)

    return wrapper
