import string
from random import choices
from datetime import datetime
from flask import request
from app import db
from passlib.apps import custom_app_context as pwd


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(5), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
        short_url = ''.join(choices(characters, k=5))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()

        return short_url

    def generate_premium_link(self, word):
        short_url = word

        link = self.query.filter_by(short_url=short_url).first()
        if link:
            return link.short_url

        self.short_url = short_url


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    is_premium = db.Column(db.Boolean, nullable=False, default=0)

    def hash_password(self, password):
        self.password_hash = pwd.encrypt(password)

    def verify_password(self, password):
        return pwd.verify(password, self.password_hash)

    def activate_premium(self):
        self.is_premium = 1
        db.session.commit()
