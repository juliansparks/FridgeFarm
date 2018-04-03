from flask import request, current_app as app
from app.rest import api
from functools import wraps
import jwt


def token_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):

        if 'X-API-KEY' not in request.headers:
            return {'message': 'Token is missing.'}, 401

        token = request.headers['X-API-KEY']

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
        except:
            return {'message': 'Token is invalid'}, 403

        return func(*args, **kwargs)

    return decorated


class classproperty(object):
    """ A decorator to create a class property """

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


from .fridges import api as fridge_api
api.add_namespace(fridge_api)

from .auth import api as auth_api
api.add_namespace(auth_api)
