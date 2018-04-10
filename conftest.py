from app import create_app
from flask_testing import TestCase
import config

# @pytest.fixture
# def app():
#     return create_app(TestConfig)

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
