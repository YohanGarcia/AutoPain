
from sqlalchemy.orm import relationship
from datetime import datetime
from src import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  nullable=False)
    lastname = db.Column(db.String(80),  nullable=False)
    telefono = db.Column(db.String(80),  nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='activo')

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('clientes', lazy=True))

    vehiculos = relationship('Vehiculo', back_populates='clientes')
    
    def __init__(self, username, lastname, telefono, user_id) -> None:
        self.username = username
        self.lastname = lastname
        self.telefono = telefono
        self.user_id = user_id

    def __repr__(self):
        return '<Cliente %r>' % self.username