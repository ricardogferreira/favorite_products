from functools import wraps

from flask_restx import abort


def basic_authentication():
    ...


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, "authenticated", True):
            return func(*args, **kwargs)

        acct = basic_authentication()  # custom account lookup function
        if acct:
            return func(*args, **kwargs)

        abort(401)

    return wrapper
