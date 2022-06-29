from flask_login import UserMixin
from sqlalchemy.orm import relationship

from src import db
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    empresa = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    servicios = relationship("Servicio", back_populates="users")

    def __init__(self, username, lastname, empresa, email, password) -> None:
        self.username = username
        self.lastname = lastname
        self.empresa = empresa
        self.email = email
        self.password = password
 
    def __repr__(self):
        return '<User %r>' % self.username