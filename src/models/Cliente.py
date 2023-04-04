from sqlalchemy.orm import relationship
from datetime import datetime
from src import db


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    telefono = db.Column(db.String(80))
    cedula = db.Column(db.String(80))
    direccion = db.Column(db.String(100))

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=True)
    
    vehiculos = relationship('Vehiculo', back_populates='clientes')
    serviciopagos = relationship('Serviciopago', back_populates='clientes')

    def __repr__(self):
        return '<Cliente %r>' % self.username