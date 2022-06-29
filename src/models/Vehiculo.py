from sqlalchemy.orm import relationship

from src import db
from datetime import datetime

class Vehiculo(db.Model):
    __tablename__ = "vehiculos"
    id = db.Column(db.Integer, primary_key=True)

    placa = db.Column(db.String(50))
    age = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    
    marca_id = db.Column(db.Integer, db.ForeignKey("marcas.id"))
    marcas = relationship("Marca", back_populates="vehiculos")
    
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelos.id"))
    modelos = relationship("Modelo", back_populates="vehiculos")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='activo')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('vehiculos', lazy=True))

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    clientes = relationship("Cliente", back_populates="vehiculos")

    servicios = relationship("Servicio", back_populates="vehiculos")

    def __init__(self, marca_id, modelo_id, cliente_id, user_id, placa, age, color) -> None:
        self.marca_id = marca_id,
        self.modelo_id = modelo_id,
        self.cliente_id = cliente_id,
        self.user_id = user_id
        self.placa = placa
        self.age = age
        self.color = color

    