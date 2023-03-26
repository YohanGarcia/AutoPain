from datetime import datetime
from src import db
from sqlalchemy.orm import relationship


class Trabajo(db.Model):
    __tablename__ = "trabajos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    trabajoprecios = relationship("TrabajoPrecio", back_populates='trabajos')
    asignaciones = relationship("Asignacion", back_populates='trabajos')
    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

class TrabajoPrecio(db.Model):
    __tablename__ = "trabajoprecios"
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Integer, nullable=False)

    trabajo_id = db.Column(db.Integer, db.ForeignKey("trabajos.id"), nullable=False)
    trabajos = relationship("Trabajo", back_populates="trabajoprecios")

    asignaciones = relationship("Asignacion", back_populates='trabajoprecios')
    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True) 