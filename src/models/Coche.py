from sqlalchemy.orm import relationship
from datetime import datetime
from src import db

class Marca(db.Model):
    __tablename__ = "marcas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    modelos = relationship("Modelo", back_populates="marcas")
    vehiculos = relationship('Vehiculo', back_populates='marcas')

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True) 
    
    def __init__(self, name) -> None:
        self.name = name
    def __repr__(self) -> str:
        return  self.name

class Modelo(db.Model):
    __tablename__ = "modelos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    marca_id = db.Column(db.Integer, db.ForeignKey("marcas.id"), nullable=False)
    marcas = relationship("Marca", back_populates="modelos")

    vehiculos = relationship('Vehiculo', back_populates='modelos')

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

    def __init__(self, name, marca_id) -> None:
        self.name = name
        self.marca_id = marca_id
    def __repr__(self) -> str:
        return self.name