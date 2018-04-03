from flask import Blueprint

bp = Blueprint('main', __name__)


def register_view(cls):
    cls.register(bp)
    return cls

from app.main import routes
