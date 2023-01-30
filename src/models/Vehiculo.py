from sqlalchemy.orm import relationship
from datetime import datetime
from src import db

class Vehiculo(db.Model):
    __tablename__ = "vehiculos"
    id = db.Column(db.Integer, primary_key=True)

    placa = db.Column(db.String(50))
    age = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    matricula = db.Column(db.String(50))

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)
    
    marca_id = db.Column(db.Integer, db.ForeignKey("marcas.id"))
    marcas = relationship("Marca", back_populates="vehiculos")
    
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelos.id"))
    modelos = relationship("Modelo", back_populates="vehiculos")

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    clientes = relationship("Cliente", back_populates="vehiculos")

    servicios = relationship("Servicio", back_populates="vehiculos")

    historialventas = relationship("HistorialVentas", back_populates="vehiculos")