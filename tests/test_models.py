from app import db
from tests.conftest import BasicTest
from app.models import User, load_user
# from flask_testing import TestCase
import pytest


class DBTest(BasicTest):
    """ Class to test SQLAlchemy models """

    def setUp(self):
        """ Create all Tables in the DB """
        db.create_all()

    def tearDown(self):
        """ Drop All Tables """
        db.session.remove()
        db.drop_all()


class TestUser(DBTest):

    @staticmethod
    def add_new_user(username: str = 'test_dude',
                     email: str = 'dude@example.com') -> User:
        """
        Create a new user and add it the DB

        Should probably be a pytest fixture
        """
        user = User(username=username, email=email)
        user.set_password('Password123')
        db.session.add(user)
        db.session.commit()
        return user

    def test_get_by_username(self):
        """
        Test that :func:`app.models.User.get_by_username` can retrive
        a user by it's username.
        """
        user = self.add_new_user()
        assert User.get_by_username(user.username) is user

    def test_password(self):
        """
        Test that :func:`app.models.User.set_password` correctly sets
        a password and that :func:`app.models.User.check_password`
        returns True for set password and False otherwise.
        """
        from werkzeug.security import check_password_hash

        user = self.add_new_user()

        #: set the user's password using :func:`app.models.User.set_password`
        user.set_password('Password123')

        #: check that the user's password matches the password that was set
        assert check_password_hash(user.password_hash, 'Password123') is True

        #: check that some other password does not match the password
        #: that was set
        assert check_password_hash(user.password_hash, 'password123') is False

        #: check that :func:`app.models.User.check_password` returns
        #: True for the correct password
        assert user.check_password('Password123') is True

        #: check that :func:`app.models.User.check_password` returns
        #: False for the wrong password
        assert user.check_password('password123') is False

    def test_existing_username(self):
        """
        Test that adding a user with an existsing username results in
        an exception
        """
        import sqlalchemy

        self.add_new_user(username='bob123', email='bob@example.com')

        #: make sure that an exception is raised
        try:
            with pytest.raises(sqlalchemy.exc.IntegrityError):
                self.add_new_user(username='bob123', email='bob2@example.com')
        except (sqlalchemy.exc.IntegrityError):
            pass

    def test_repr__(self):
        """
        Test :func:`app.models.User.__repr__`
        """
        user = self.add_new_user(username='bob123', email='bob@example.com')
        assert repr(user) == '<User bob123>'

    def test_load_user(self):
        """
        Test that :func:`app.models.load_user` returns the correct user
        """
        user = self.add_new_user()

        assert load_user(str(user.id)) is user
