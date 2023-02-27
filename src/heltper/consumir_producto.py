from flask import flash, redirect
from src import db


from src.models.Productos import HistorialVentas, InventarioProducto

def Consumir_producto(id_vehiculo, id_servicios, id_productos, id_cantidad_unidades, cantidad, id_empleados,precio_venta, ruta):
    venta = HistorialVentas()
    inventario_status = InventarioProducto()
    inventario = InventarioProducto.query.filter_by(id=id_productos).first()
    producto_venta = HistorialVentas.query.filter_by(id_inventario_productos=inventario.id).all()
    if producto_venta:
        for producto in producto_venta:
            cantidad_vendidas = producto.cantidad
            cantidad_inventario = inventario.cantidad
            resultado = cantidad_vendidas + cantidad

            if resultado > cantidad_inventario:
                disponibles = (cantidad_vendidas - cantidad_inventario)
                flash(f'Solo hay {disponibles} {inventario.productos.name} {inventario.productos.descrition} disponible ') 
                return redirect(ruta)
            elif resultado == cantidad_inventario:
                venta.id_vehiculos = id_vehiculo
                venta.id_servicios = id_servicios
                venta.id_inventario_productos = id_productos
                venta.cantidad = cantidad
                venta.id_cantidad_unidades = id_cantidad_unidades
                venta.id_empleados = id_empleados
                venta.precio = precio_venta
                db.session.add(venta)
                inventario.status = False
                db.session.commit()
                flash('Producto Consumido con exicto!')
                return redirect(ruta)

            print(f'cantidad vendidos: {resultado}')
            print(f'cantidad de product: {cantidad_inventario}')

    else:
        print('No se a vendido de producto')
    print(f'inventario: {inventario.id}')
    try:
        
        venta.id_vehiculos = id_vehiculo
        venta.id_servicios = id_servicios
        venta.id_inventario_productos = id_productos
        venta.cantidad = cantidad
        venta.id_cantidad_unidades = id_cantidad_unidades
        venta.id_empleados = id_empleados
        venta.precio = precio_venta
        # db.session.add(venta)
        # db.session.commit()
        flash('Producto Consumido con exicto!')
        return redirect(ruta)
    except Exception as e:
        print(e)
