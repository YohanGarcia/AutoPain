from flask import (
    jsonify, render_template, Blueprint, flash,
    redirect, request, session, url_for
)

from flask_login import login_required

from src import db
from src.helper import current_date_format
from src.heltper.consumir_producto import Consumir_producto
from src.heltper.formato import format_number

from src.models.Productos import Unidad, Producto, InventarioProducto, HistorialVentas, CantidadUnidad
from src.models.Servicio import Servicio
from src.models.Empleados import Empleado
from src.models.Vehiculo import Vehiculo
from src.models.Asignacion import Asignacion
producto = Blueprint('producto', __name__, url_prefix='/productos')


@producto.route('/')
@login_required
def index():
    query_productos = Producto.query.all()
    query_unidad = Unidad.query.all()
    query_historial = HistorialVentas.query.all()
    query_inventario = InventarioProducto.query.all()

    productos_vendidos = {}
    for inventario_producto in query_inventario:
        total_ventas = 0.0
        for venta in query_historial:
            if inventario_producto.productos.id == venta.id_productos:
                total_ventas += venta.cantidad
        productos_vendidos[inventario_producto.productos.name, inventario_producto.productos.descrition, inventario_producto.cantidad] = total_ventas
    
    return render_template(
        'productos/index.html',
        productos=query_productos,
        unidad=query_unidad,
        historial_ventas=query_historial,
        inventarios=query_inventario,
        current_date_format=current_date_format,
        format_number=format_number,
        productos_vendidos=productos_vendidos
    )


@producto.route('/registrar/nuevo', methods=['GET', 'POST'])
@login_required
def registrar_nuevo():
    query_unidad = Unidad.query.all()
    query_productos = Producto.query.all()
    if request.method == 'POST':
        try:
            producto = Producto()
            producto.name = request.form.get('name').upper()
            producto.descrition = request.form.get('descripcion').upper()
            producto.precio = request.form.get('precio')
            producto.id_unidad = request.form.get('unidad')

            db.session.add(producto)
            db.session.commit()

            flash('Producto Creado con exicto!', 'success')
            return redirect(url_for('producto.registrar_nuevo'))

        except Exception as e:
            print(e)
    return render_template('productos/registrar_nuevo.html',
                unidad=query_unidad, productos=query_productos,
                current_date_format=current_date_format,
                format_number=format_number)


@producto.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        invetario = InventarioProducto()
        print('1')
        try:
            id_producto = request.form.get('producto')
            id_cantidad_unidades = request.form.get('cantidad')
            cantidad = float(request.form.get('cantidades'))
            print('2')
            

            query_inventario = InventarioProducto.query.filter_by(id_producto=id_producto).first()

            if not query_inventario:
                print('3')
                invetario.id_producto = id_producto
                invetario.id_cantidad_unidades = id_cantidad_unidades
                invetario.cantidad = cantidad
            
                db.session.add(invetario)
                db.session.commit()
                flash('Producto Creado con exicto!', 'success')

            else:
                print('4')
                query_inventario.cantidad = query_inventario.cantidad + cantidad
                db.session.commit()
                flash('Producto Acualizado!', 'success')
            
        except Exception as e:
            print(e)
        return redirect(url_for('producto.index'))


@producto.route('/carbrand', methods=['POST', 'GET'])
def carbram():
    print('Entro aqui 3')
    if request.method == 'POST':
        poducto_id = request.form['marca_id']
        result = Producto.query.filter_by(id=poducto_id).first()
        query = CantidadUnidad.query.filter_by(
            id_unidad=result.unidades.id).all()
        print('Endro aqui en producto')
        print('================================')
        print(result.unidades.typo)
        OutputArray = []
        for row in query:
            outputObj = {
                'id': row.id,
                'name': row.name
            }
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


@producto.route('/unidad', methods=['GET', 'POST'])
@login_required
def unidad():
    query_unidad = Unidad.query.all()
    query_cantidad_unidad = CantidadUnidad.query.all()
    if request.method == 'POST':
        try:
            unidad = CantidadUnidad()
            unidad.name = request.form.get('name')
            unidad.unidad = request.form.get('unidad')
            unidad.id_unidad = request.form.get('typo')

            db.session.add(unidad)
            db.session.commit()
            flash('Producto Creado con exicto!', 'success')
            return redirect(url_for('producto.unidad'))
        except Exception as e:
            print(e)
            return redirect(url_for('producto.unidad'))

    return render_template('productos/unidad.html',
            unidades=query_unidad,
            cantidad_unidad=query_cantidad_unidad,
            current_date_format=current_date_format,
            format_number=format_number)


@producto.route('/consumir', methods=['GET', 'POST'])
@login_required
def consumir():
    query_servicio = Servicio.query.filter_by(status=True).all()
    query_vehiculo = Vehiculo.query.filter_by(status=True).all()
    query_empleados = Empleado.query.filter_by(status=True).all()
    query_productos = Producto.query.filter_by(status=True).all()
    query_historia_ventas = HistorialVentas.query.filter_by(status=True).all()

    if request.method == 'POST':
        # try:
        #     venta = HistorialVentas()
        #     print('Id product: ', request.form.get('id_empleados'))
        #     print('Id Vehiculo: ', request.form.get('id_vehiculos'))
        #     print('Id Servicio: ', request.form.get('id_servicios'))
        #     print('Id Producto: ', request.form.get('producto'))
        #     print('Unidad: ', request.form.get('cantidad'))
        #     print('Cantidades: ', request.form.get('cantidades'))

        #     venta.id_empleados = request.form.get('id_empleados')
        #     venta.id_vehiculos = request.form.get('id_vehiculos')
        #     venta.id_servicios = request.form.get('id_servicios')
        #     venta.id_productos = request.form.get('producto')
        #     venta.cantidad = request.form.get('cantidades')
        #     venta.id_cantidad_unidades = request.form.get('cantidad')

        #     db.session.add(venta)
        #     db.session.commit()
        #     flash('success','Se comusumio el producto')
        #     return redirect(url_for('producto.consumir'))
        # except Exception as e:
        #     print(e)
        # return redirect(url_for('producto.consumir'))
        id_vehiculos = request.form.get('id_vehiculos')
        id_servicios = request.form.get('id_servicios')
        id_productos = request.form.get('producto')
        id_cantidad_unidades = request.form.get('cantidad')
        id_empleados = request.form.get('id_empleados')
        precio_venta = request.form.get('precio_venta')
        ruta = request.form.get('ruta')
        cantidad = request.form.get('cantidades')
        cantidad2 = request.form.get('cantidades2')
        print(f'cantidad {cantidad}')
        print(f'Cantidad2 {cantidad2}')


        if id_vehiculos is None:
            flash('selecione el vehiculo')
            return redirect(ruta)
        elif id_servicios is None:
            flash('selecione el servicio')
            return redirect(ruta)
        elif id_productos is None:
            flash('selecione el producto')
            return redirect(ruta)
        
        elif id_empleados is None:
            flash('selecione el enpleado')
            return redirect(ruta)
        elif precio_venta is None:
            flash('ingrese el precio de venta')
            return redirect(ruta)
        elif cantidad != '':
            return Consumir_producto(
                id_vehiculo=id_vehiculos,
                id_servicios=id_servicios,
                id_productos=id_productos,
                id_cantidad_unidades=id_cantidad_unidades,
                cantidad=float(cantidad),
                id_empleados=id_empleados,
                precio_venta=precio_venta,
                ruta=ruta
            )
        elif cantidad2 is not None:
            return Consumir_producto(
                id_vehiculo=id_vehiculos,
                id_servicios=id_servicios,
                id_productos=id_productos,
                id_cantidad_unidades=id_cantidad_unidades,
                cantidad=float(cantidad2),
                id_empleados=id_empleados,
                precio_venta=precio_venta,
                ruta=ruta
            )
       
    return render_template('productos/consumir.html', 
                            servicios=query_servicio, vehiculos=query_vehiculo,
                            empleados=query_empleados, productos=query_productos,
                            ventas=query_historia_ventas,current_date_format=current_date_format,
                            format_number=format_number, ruta=request.path,)


@producto.route('/ventas/servicios', methods=['POST', 'GET'])
def ventas():
    print('Entro aqui 3')
    if request.method == 'POST':
        vehiculo = request.form['marca_id']
        query = Servicio.query.filter_by(
            vehiculo_id=vehiculo, status=True).all()
        print('Endro aqui en ventas')
        print('================================')
        OutputArray = []
        for row in query:
            outputObj = {
                'id': row.id,
                'name': row.serviciolistas.name
            }
            OutputArray.append(outputObj)
    return jsonify(OutputArray)

# @producto.route('/ventas/empleados', methods=['POST', 'GET'])
# def ventas_empleados():
#     print('Entro aqui 3')
#     if request.method == 'POST':
#         servicio_id = request.form['marca_id']
#         query =  Empleado.query.all()
#         print('Endro aqui en ventas empleados')
#         print('================================')
#         OutputArray = []
#         for row in query:

#             outputObj = {
#                 'id': row.id,
#                 'name': row.empleados.name
#             }
#             OutputArray.append(outputObj)
#     return jsonify(OutputArray)
