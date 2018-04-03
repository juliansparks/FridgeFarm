from flask_restplus import Namespace, Resource
from flask import request, current_app as app, make_response
from functools import wraps
from app.models import User
import jwt
import datetime

api = Namespace('auth', description='Login to get API token')


@api.route('/login')
class LoginResource(Resource):
    """ Endpoint to login and get api token """

    def get(self):
        auth = request.authorization

        if auth:
            user = User.get_by_username(auth.username)

            if user and user.check_password(auth.password):
                token = jwt.encode(
                    {
                        'username':
                        auth.username,
                        'exp':
                        datetime.datetime.utcnow() +
                        datetime.timedelta(minutes=5)
                    },
                    app.config['SECRET_KEY'])
                return {'token': token.decode('UTF-8')}

        return make_response(
            'Could not verify!', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})


def token_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                print(data)
            except:
                return {'message': 'Token is invalid'}, 403

            if not data:
                return {'message': 'Token is missing.'}, 401

        return func(*args, **kwargs)

    return decorated
