from flask_login import UserMixin
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = self.__create_password(password)
        self.email = email

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)