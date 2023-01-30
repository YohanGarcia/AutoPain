from datetime import datetime
from sqlalchemy.orm import relationship
from src import db

class Unidad(db.Model):
    __tablename__ = "unidades"
    id = db.Column(db.Integer, primary_key=True)

    typo = db.Column(db.String(50), nullable=False)
    productos = relationship("Producto", back_populates="unidades")
    cantidad_unidades = relationship("CantidadUnidad", back_populates="unidades")

class CantidadUnidad(db.Model):
    __tablename__ = "cantidad_unidades"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    unidad = db.Column(db.Float, nullable=False)

    id_unidad = db.Column(db.Integer, db.ForeignKey("unidades.id"), nullable=False)
    unidades = relationship("Unidad", back_populates="cantidad_unidades")

    inventarioproductos = relationship("InventarioProducto", back_populates="cantidad_unidades")
    historialventas = relationship("HistorialVentas", back_populates="cantidad_unidades")
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    descrition = db.Column(db.String(50))
    precio = db.Column(db.Float, nullable=False)

    id_unidad = db.Column(db.Integer, db.ForeignKey("unidades.id"), nullable=False)
    unidades = relationship("Unidad", back_populates="productos")

    inventarioproductos = relationship("InventarioProducto", back_populates="productos")
    historialventas = relationship("HistorialVentas", back_populates="productos")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

class InventarioProducto(db.Model):
    __tablename__ = "inventarioproductos"
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=True)
    
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=True)
    id_cantidad_unidades = db.Column(db.Integer, db.ForeignKey("cantidad_unidades.id"), nullable=True)

    cantidad_unidades = relationship("CantidadUnidad", back_populates="inventarioproductos")
    productos = relationship("Producto", back_populates="inventarioproductos")
    

class HistorialVentas(db.Model):
    __tablename__ = "historialventas"
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=True)
    precio = db.Column(db.Float, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, unique=False, default=True)

    id_productos = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    productos = relationship("Producto", back_populates="historialventas")

    id_empleados = db.Column(db.Integer, db.ForeignKey("empleados.id"), nullable=False)
    empleados = relationship("Empleado", back_populates="historialventas")

    id_vehiculos = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    vehiculos = relationship("Vehiculo", back_populates="historialventas")

    id_servicios = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)
    servicios = relationship("Servicio", back_populates="historialventas")

    id_cantidad_unidades = db.Column(db.Integer, db.ForeignKey("cantidad_unidades.id"), nullable=True)
    cantidad_unidades = relationship("CantidadUnidad", back_populates="historialventas")