from sqlalchemy.orm import relationship
from datetime import datetime
from src import db

class Asignacion(db.Model):
    __tablename__ = 'asignaciones'
    id = db.Column(db.Integer, primary_key=True)
    pagado = db.Column(db.Boolean, default=False)

    empleado_id = db.Column(db.Integer, db.ForeignKey("empleados.id"))
    empleados = relationship("Empleado", back_populates="asignaciones")
    
    trabajo_id = db.Column(db.Integer, db.ForeignKey("trabajos.id"))
    trabajos = relationship("Trabajo", back_populates="asignaciones")

    trabajoprecio_id = db.Column(db.Integer, db.ForeignKey("trabajoprecios.id"))
    trabajoprecios = relationship("TrabajoPrecio", back_populates="asignaciones")

    serviciopieza_id = db.Column(db.Integer, db.ForeignKey("serviciopiezas.id"))
    serviciopiezas = relationship("Serviciopieza", back_populates="asignaciones")

    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"))
    servicios = relationship("Servicio", back_populates="asignaciones")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)