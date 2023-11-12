from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .login import login_manager

users_database = SQLAlchemy()


class User(UserMixin, users_database.Model):
    id = users_database.Column(users_database.String(32), primary_key=True)
    username = users_database.Column(users_database.String(128), unique=True, nullable=False)

    @login_manager.user_loader
    def load_user(self):
        return User.query.get(self.id)


class Passwords(users_database.Model):
    id = users_database.Column(users_database.String(32), users_database.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    r = users_database.Column(users_database.Integer, primary_key=True)
    password = users_database.Column(users_database.String(512), nullable=False)


class Attempts(users_database.Model):
    id = users_database.Column(users_database.String(32), users_database.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    r = users_database.Column(users_database.Integer, primary_key=True)
    attempts = users_database.Column(users_database.Integer, nullable=False)
    successes = users_database.Column(users_database.Integer, nullable=False)
