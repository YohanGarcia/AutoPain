from src import db
from sqlalchemy.orm import relationship
from datetime import datetime


class Empleado(db.Model):
    __tablename__ = "empleados"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50))
    telefono = db.Column(db.String(50), unique=True)
    telefonocasa = db.Column(db.String(50))
    cedula = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    foto = db.Column(db.Text)
    nacimiento = db.Column(db.String(50))

    asignaciones = relationship("Asignacion", back_populates="empleados")
    historialventas = relationship("HistorialVentas", back_populates="empleados")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

    def __repr__(self) -> str:
        return  self.name