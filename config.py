import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    """
    This class is passed to :func:`app.create_app` and is used
    to configure flask.

    *See* `Flask documentation
    <http://flask.pocoo.org/docs/0.12/config/#configuring-from-files>`_
    """

    #: Used by flask when encryption is required.
    #:
    #: This should be set to a random string via the 'SECRET_KEY'
    #: environment variable.
    #:
    #: .. code-block:: python
    #:
    #:   SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #: The database URI that should be used for the connection; used by
    #: SQLAlchemy
    #:
    #: .. code-block:: python
    #:
    #:   SQLALCHEMY_DATABASE_URI = os.environ.get(
    #:     'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    #: 	If set to True, Flask-SQLAlchemy will track modifications of objects
    #: and emit signals. The default is None, which enables tracking but
    #: issues a warning that it will be disabled by default in the future.
    #: This requires extra memory and should be disabled if not needed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #: Weather Flask-DebugTool should intercept redirects
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    #: If you enable debug support the server will reload itself on code
    #: changes, and it will also provide you with a helpful debugger if things
    #: go wrong.
    DEBUG = False


class DevConfig(Config):
    """ Config for use during development """

    #: set debug mode
    DEBUG = True


class TestConfig(DevConfig):
    """ Config for use during testing """

    #: Set debug mode
    DEBUG = True

    #: Set testing mode
    TESTING = True

    #: Set database URI to testing db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test_app.db')
