from flask import (
    jsonify, render_template, Blueprint, flash,
    redirect, request, url_for
)
from collections import Counter

from flask_login import login_required
from src import db
from src.forms.serviciolista import ServicioListaForm
from src.helper import current_date_format
from src.heltper.empleado_total import Empleado_total
from src.heltper.enumerate_pieza import enumerate_serviciopiezas
from src.heltper.formato import format_number
from src.models.Productos import HistorialVentas, Producto, InventarioProducto

from src.models.Servicio import Servicio, Serviciolista, Servicioprecio, Serviciopieza
from src.models.Vehiculo import Vehiculo
from src.models.Pieza import Pieza, PiezaPrecio
from src.models.Asignacion import Asignacion
from src.models.Empleados import Empleado
from src.models.Trabajos import Trabajo, TrabajoPrecio

pinturadetalle = Blueprint('pintura-detalle', __name__,
                           url_prefix='/pintura/detalle')


@pinturadetalle.route('/servicio/<int:servicio_id>/vehiculo/<int:vehiculo_id>', methods=['GET', 'POST'])
@login_required
def index(servicio_id, vehiculo_id):
    vehiculo = Vehiculo.query.filter_by(id=vehiculo_id).first()
    servicio = Servicio.query.filter_by(id=servicio_id).first()
    serviciopiezas = Serviciopieza.query.filter_by(servicio_id=servicio_id).all()
    query_productos = Producto.query.filter_by(status=True).all()
    venta = HistorialVentas.query.filter_by(id_servicios=servicio_id, id_vehiculos=vehiculo_id).all()
    asignaciones = Asignacion.query.filter_by(servicio_id=servicio_id).all()
    query_hinventario_productos = InventarioProducto.query.filter_by(status=True).all()
    piezas = Pieza.query.all()
    empleados = Empleado.query.all()
    trabajos = Trabajo.query.all()

    total = 0
    for i in serviciopiezas:
        if i.pieza_precios:
            precio = i.pieza_precios.pieza_precio
            total += precio

    context = {
        'enumerate_serviciopiezas': enumerate_serviciopiezas,
        'servicio_id': servicio_id
    }

    counter = 0
    for precio in servicio.serviciopiezas:
        if precio.pieza_precio_id is not None:
            counter += precio.pieza_precios.pieza_precio

    return render_template(
        '/servicios/pintura-detalle.html',
        **context,
        total=total,
        counter=counter,
        asignaciones=asignaciones,
        vehiculo=vehiculo,
        piezas=piezas,
        empleados=empleados,
        trabajos=trabajos,
        servicio=servicio,
        serviciopiezas=serviciopiezas,
        empleados_total=Empleado_total(asignaciones),
        format_number=format_number,
        current_date_format=current_date_format,
        ruta=request.path,
        productos=query_productos,
        query_hinventario_productos=query_hinventario_productos,
        ventas=venta
    )


@pinturadetalle.route('servicio/<int:servicio_id>/pieza/precio/<int:vehiculo_id>', methods=['POST'])
@login_required
def pieza_precio(servicio_id, vehiculo_id):

    serviciopiezas = Serviciopieza.query.filter_by(
        servicio_id=servicio_id).all()

    for index, pieza in enumerate(serviciopiezas):

        pieza_id = request.form.get(f'pieza_id{index+1}')
        print(f'pieza_id: {pieza_id}')

        serviciopieza = Serviciopieza.query.filter_by(
            servicio_id=servicio_id, pieza_id=pieza_id).first()

        precio_id = request.form.get(f'id_pieza_precio{index+1}')

        if serviciopieza and serviciopieza.pieza_precio_id:
            flash('Esta piesa ya tiene un precio asignado, ')
        else:
            serviciopieza.pieza_precio_id = precio_id
            db.session.commit()
    flash('Precio agregado, sucesso')
    return redirect(url_for('pintura-detalle.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))


@pinturadetalle.route('/<int:servicio_id>/vehiculo/<int:vehiculo_id>/asignacion2', methods=['GET', 'POST'])
def asignacion_detalle(servicio_id, vehiculo_id):
    if request.method == 'POST':
        multiselect = request.form.getlist('mymultiselect')
        empleado = request.form.get('empleado')
        trabajo = request.form.get('car_trabajo')
        precio = request.form.get('car_precio')

        print(f'empleado: {empleado}',
              f'trabajo: {trabajo}', f'precio: {precio}')

        if not empleado:
            flash('Selecione un empleado')
        if not precio:
            flash('Ingrese el precio')
        if not trabajo:
            flash('Selecione un tipo de trabajo')
        if not multiselect:
            flash('Selecione las pieza')
        else:
            for pieza in multiselect:
                print(f'pieza: {pieza}')
                save = Asignacion(serviciopieza_id=pieza,
                                  trabajo_id=trabajo,
                                  empleado_id=empleado,
                                  trabajoprecio_id=precio,
                                  servicio_id=servicio_id)
                db.session.add(save)
                db.session.commit()
            flash('Registrado exictosamente!.')
    return redirect(url_for('pintura-detalle.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))

# registracion de piezas de pintura en general


@pinturadetalle.route('/<int:servicio_id>/vehiculo/<int:vehiculo_id>/servicio-pieza', methods=['GET', 'POST'])
@login_required
def pieza_create_detalle(servicio_id, vehiculo_id):
    if request.method == 'POST':
        multiselect = request.form.getlist('mymultiselect')
        if not multiselect:
            flash('Selecione las pieza')
        else:
            for pieza in multiselect:
                save = Serviciopieza(servicio_id=servicio_id, pieza_id=pieza)
                db.session.add(save)
                db.session.commit()
            flash('Piezas registrada')

    return redirect(url_for('.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))


@pinturadetalle.route('/pieza/precio', methods=['POST', 'GET'])
def carbram():
    print('Entro aqui 2 pieza')
    if request.method == 'POST':
        id_pieza = request.form['marca_id']
        print(id_pieza)
        result = PiezaPrecio.query.filter_by(id_piezas=id_pieza).all()
        OutputArray = []
        for row in result:
            outputObj = {
                'id': row.id,
                'name': row.precio
            }
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


@pinturadetalle.route("/get_cars/<trabajo_id>")
def get_cars(trabajo_id):
    print('si qeu entro aqui con existo')
    cars = TrabajoPrecio.query.filter_by(trabajo_id=trabajo_id).all()
    return jsonify([{"id": car.id, "name": car.precio} for car in cars])
