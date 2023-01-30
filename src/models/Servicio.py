from sqlalchemy.orm import relationship
from datetime import datetime
from src import db

class Servicio(db.Model):
    __tablename__ = "servicios"
    id = db.Column(db.Integer, primary_key=True)
    
    serviciolista_id = db.Column(db.Integer, db.ForeignKey("serviciolistas.id"))
    serviciolistas = relationship("Serviciolista", back_populates="servicios")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

    vehiculo_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"))
    vehiculos = relationship("Vehiculo", back_populates="servicios")

    servicioprecios = relationship("Servicioprecio", back_populates="servicios")
    serviciopiezas = relationship("Serviciopieza", back_populates="servicios")
    asignaciones = relationship("Asignacion", back_populates="servicios")
    serviciopagos = relationship("Serviciopago", back_populates="servicios")
    historialventas = relationship("HistorialVentas", back_populates="servicios")
    
class Serviciolista(db.Model):
    __tablename__ = "serviciolistas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    servicios = relationship("Servicio", back_populates="serviciolistas")

class Servicioprecio(db.Model):
    __tablename__ = "servicioprecios"
    id = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Integer)
    
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"))
    servicios = relationship("Servicio", back_populates="servicioprecios")

class Serviciopieza(db.Model):
    __tablename__ = 'serviciopiezas'
    id = db.Column(db.Integer, primary_key=True)

    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"))
    servicios = relationship("Servicio", back_populates="serviciopiezas")

    pieza_id = db.Column(db.Integer, db.ForeignKey("piezas.id"))
    piezas = relationship("Pieza", back_populates="serviciopiezas")

    pieza_precio_id = db.Column(db.Integer, db.ForeignKey("pieza_precios.id"))
    pieza_precios = relationship("PiezaPrecio", back_populates="serviciopiezas")

    asignaciones = relationship("Asignacion", back_populates="serviciopiezas")
    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

class Serviciopago(db.Model):
    __tablename__ = 'serviciopagos'
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Integer)
    descripcion = db.Column(db.String)

    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"))
    servicios = relationship("Servicio", back_populates="serviciopagos")

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    clientes = relationship("Cliente", back_populates="serviciopagos")
    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)