from flask import Blueprint
from flask_restplus import Api

bp = Blueprint('rest', __name__, url_prefix='/api/v1')

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    bp,
    doc='/doc',
    version='1.0',
    description='REST API',
    authorizations=authorizations)

from app.rest import apis
