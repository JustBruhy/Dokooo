from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from hashlib import sha256
db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def check_password(self, password):
        return self.password == sha256(password.encode("utf-8")).hexdigest()

    def set_password(self, new_password):
        self.password = sha256(new_password.encode("utf-8")).hexdigest()

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.password})"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(90), unique=False, nullable=False)

    def __repr__(self):
        return f"Article({self.id}, {self.title}, {self.body}, {self.username})"
