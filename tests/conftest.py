from app import create_app, db as _db
from app.models import Fridge, Item, User
from flask_testing import TestCase
# from pytest_selenium import EventFiringWebDriver
from urllib.parse import urlparse
import config
import pytest
import os


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    return chrome_options


@pytest.fixture(scope='function')
def selenium(driver):
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


@pytest.fixture(scope='session')
def app(request):
    """" Session wide test Flask application """
    app = create_app(config.TestConfig)

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """" Session wide test database """
    uri = urlparse(app.config['SQLALCHEMY_DATABASE_URI'])
    if uri.path and os.path.exists(uri.path):
        os.unlink(uri.path)

    _db.app = app
    _db.create_all()

    def teardown():
        _db.drop_all()
        if uri.path:
            os.unlink(uri.path)

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def uncommited_user():
    user = User(username='MrTest', email='mrtest@example.com')
    user.set_password('Password123')
    return user


@pytest.fixture(scope='function')
def user(session, uncommited_user):
    session.add(uncommited_user)
    session.commit()
    return uncommited_user


@pytest.fixture(scope='function')
def uncommited_fridge(user):
    fridge = Fridge(name='TestFridge', descripton='A fake fridge')
    fridge.user_id = user.id


@pytest.fixture(scope='function')
def fridge(session, uncommited_fridge):
    session.add(fridge)
    session.commit()
    return uncommited_fridge


@pytest.fixture(scope='function')
def uncommited_item(user, fridge):
    item = Item(name='Apples', description='red; round', quantity=1)
    item.user_id = user.id
    item.fridge_id = fridge.id
    return item


@pytest.fixture(scope='function')
def item(user, uncommited_item):
    session.add(uncommited_item)
    session.commit()
    return uncommited_item


#: Set the class from config to be used during testing
Conf = config.DevConfig


class BasicTest(TestCase):
    """
    Class to test SQLAlchemy models

    :ivar SQLALCHEMY_DATABASE_URI: initial value: Conf.SQLALCHEMY_DATABASE_URI
    """

    SQLALCHEMY_DATABASE_URI = Conf.SQLALCHEMY_DATABASE_URI

    TESTING = True

    def create_app(self):
        """
        Returns an instance of the app for use in tests
        """
        return create_app(Conf)

    def setUp(self):
        """ Initialize the app and assign test variables """

        # self.client = self.app.test_client  #: initial value: 'par1'

    def tearDown(self):
        """ Terminate the app """
        pass
