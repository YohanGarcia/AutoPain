from datetime import datetime
from src import db
from sqlalchemy.orm import relationship


class Pieza(db.Model):
    __tablename__ = "piezas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

    serviciopiezas = relationship("Serviciopieza", back_populates="piezas")
    pieza_precios = relationship("PiezaPrecio", back_populates="piezas")

    def __init__(self, name) -> None:
        self.name = name
    def __repr__(self) -> str:
        return  self.name

class PiezaPrecio(db.Model):
    __tablename__ = 'pieza_precios'
    id = db.Column(db.Integer, primary_key=True)
    pieza_precio = db.Column(db.Float, nullable=False)
    
    id_piezas = db.Column(db.Integer, db.ForeignKey("piezas.id"), nullable=False)
    piezas = relationship("Pieza", back_populates="pieza_precios")

    serviciopiezas = relationship("Serviciopieza", back_populates="pieza_precios")
  
