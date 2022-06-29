from operator import truth
from src import db
from sqlalchemy.orm import relationship
from datetime import datetime


class Lista(db.Model):
    __tablename__ = "listas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    servicios = relationship("Servicio", back_populates="listas")

    def __init__(self, name) -> None:
        self.name = name
    def __repr__(self) -> str:
        return  self.name

class Servicio(db.Model):
    __tablename__ = "servicios"
    id = db.Column(db.Integer, primary_key=True)
    lista_id = db.Column(db.Integer, db.ForeignKey("listas.id"), nullable=True)
    listas = relationship("Lista", back_populates="servicios")

    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='activo')

    vehiculo_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"))
    vehiculos = relationship("Vehiculo", back_populates="servicios")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = relationship('User', back_populates='servicios')

    pinturageneral = relationship("Pinturageneral", back_populates="servicios")

class Pinturageneral(db.Model):
    __tablename__ = "pinturageneral"
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Integer)
    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='activo')

    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"))
    servicios = relationship("Servicio", back_populates="pinturageneral")

    pinturageneralpiesas = relationship("Pinturageneralpiesa", back_populates=("pinturageneral"))

class Pinturageneralpiesa(db.Model):
    __tablename__ = "pinturageneralpiesas"
    id = db.Column(db.Integer, primary_key=True)

    piesa_id = db.Column(db.Integer, db.ForeignKey("piesas.id"), nullable=False)
    piesas = relationship("Piesa", back_populates=("pinturageneralpiesas"))

    pinturageneral_id = db.Column(db.Integer, db.ForeignKey("pinturageneral.id"))
    pinturageneral = relationship("Pinturageneral", back_populates=("pinturageneralpiesas"))

    def __repr__(self) -> str:
        return self.id