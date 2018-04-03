from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

import typing


@login.user_loader
def load_user(id: str) -> 'User':
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fridges = db.relationship('Fridge', backref='owner', lazy='dynamic')

    @staticmethod
    def get_by_username(username: str) -> 'User':
        return User.query.filter_by(username=username).first()

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Fridge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(140))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='fridge', lazy='dynamic')

    @staticmethod
    def by_id(fridge_id: typing.Union[int, str]) -> 'Fridge':
        return Fridge.query.filter_by(id=fridge_id).first_or_404()

    def update(self, dic):
        """ Update fridge from values in dict """
        for key, value in dic.items():
            if getattr(self, key, None):
                setattr(self, key, value)
        db.session.commit()

    def remove(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def add_item(self,
                 name: str,
                 description: str,
                 quantity: int = 1,
                 expiration: datetime = datetime.max) -> None:
        item = Item(
            name=name,
            description=description,
            quantity=quantity,
            experation=expiration,
            fridge_id=self.id,
            user_id=self.user_id)
        db.session.add(item)
        db.session.commit()
        return item
    
    def __contains__(self, item: 'Item') -> bool:
        return item in self.items

    def __repr__(self) -> str:
        return f'<Fridge {self.id}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(140))
    quantity = db.Column(db.Integer)
    experation = db.Column(db.DateTime, index=True, default=datetime.max)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'))

    @staticmethod
    def by_id(item_id: typing.Union[int, str]) -> 'Item':
        return Item.query.filter_by(id=item_id).first_or_404()

    def remove(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @hybrid_property
    def expired(self) -> bool:
        return self.experation < datetime.today()

    @hybrid_property
    def has_expiration(self) -> bool:
        return not self.experation == datetime.max

    def __repr__(self) -> str:
        return f'<Item {self.id}>'
