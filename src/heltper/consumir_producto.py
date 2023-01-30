from flask import flash, redirect
from src import db


from src.models.Productos import HistorialVentas


def Consumir_producto(id_vehiculo, id_servicios, id_productos, id_cantidad_unidades, cantidad, id_empleados,precio_venta, ruta):
    venta = HistorialVentas()
    try:
        
        venta.id_vehiculos = id_vehiculo
        venta.id_servicios = id_servicios
        venta.id_productos = id_productos
        venta.cantidad = cantidad
        venta.id_cantidad_unidades = id_cantidad_unidades
        venta.id_empleados = id_empleados
        venta.precio = precio_venta
        db.session.add(venta)
        db.session.commit()
        flash('Producto Consumido con exicto!')
        return redirect(ruta)
    except Exception as e:
        print(e)
