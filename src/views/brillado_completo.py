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
from src.heltper.formato import format_number
from src.models.Productos import HistorialVentas, Producto

from src.models.Servicio import Servicio, Serviciolista, Servicioprecio, Serviciopieza
from src.models.Vehiculo import Vehiculo
from src.models.Pieza import Pieza, PiezaPrecio
from src.models.Asignacion import Asignacion
from src.models.Empleados import Empleado
from src.models.Trabajos import Trabajo, TrabajoPrecio

brilado_completo = Blueprint('brillado-completo', __name__,
                           url_prefix='/brillado/completo')


@brilado_completo.route('/servicio/<int:servicio_id>/vehiculo/<int:vehiculo_id>', methods=['GET', 'POST'])
@login_required
def index(servicio_id, vehiculo_id):
    vehiculo = Vehiculo.query.filter_by(id=vehiculo_id).first()
    servicio = Servicio.query.filter_by(id=servicio_id).first()
    serviciopiezas = Serviciopieza.query.filter_by(servicio_id=servicio_id).all()
    asignaciones = Asignacion.query.filter_by(servicio_id=servicio_id).all()
    query_productos = Producto.query.filter_by(status=True).all()
    venta = HistorialVentas.query.filter_by(status=True, id_servicios=servicio_id, id_vehiculos=vehiculo_id).all()
    piezas = Pieza.query.filter_by(name='Brillado Completo').first()
    empleados = Empleado.query.all()
    trabajos = Trabajo.query.all()



    query_servicio_piezas = Serviciopieza.query.filter_by(servicio_id=servicio_id, pieza_id = piezas.id).first()

    if query_servicio_piezas:
       pass
    else:
        save = Serviciopieza()
        save.servicio_id = servicio_id
        save.pieza_id = piezas.id

        db.session.add(save)
        db.session.commit()
        return redirect(url_for('.index',servicio_id=servicio_id, vehiculo_id=vehiculo_id))
    counter = 0
    for precio in servicio.servicioprecios:
        if precio.precio is not None:
            counter += precio.precio

    return render_template(
        '/servicios/brillado-completo.html',
        asignaciones=asignaciones,
        counter=counter,
        vehiculo=vehiculo,
        piezas=piezas,
        empleados=empleados,
        trabajos=trabajos,
        servicio=servicio,
        serviciopiezas=serviciopiezas,
        productos=query_productos,
        ventas=venta,
        ruta=request.path,
        empleados_total=Empleado_total(asignaciones),
        format_number=format_number,
        current_date_format=current_date_format
    )


@brilado_completo.route('/emplado/<int:empleado_id>/trabajo/<int:trabajo_id>/serviciopieza/<int:serviciopieza_id>/servicio/<int:servicio_id>/vehiculo/<int:vehiculo_id>')
@login_required
def delete_asignacion(empleado_id, trabajo_id,serviciopieza_id,servicio_id, vehiculo_id):
    asignacones = Asignacion.query.filter_by(
                        empleado_id=empleado_id,
                        trabajo_id=trabajo_id,
                        serviciopieza_id=serviciopieza_id,
                        servicio_id=servicio_id, 
                        ).first()
    print(f'empleado: {empleado_id}')
    print(f'trabajo: {trabajo_id}')
    print(f'servicio pieza: {serviciopieza_id}')
    print(f'servicio: {servicio_id}')
    print(f'vehiculo: {vehiculo_id}')
    if asignacones:
        db.session.delete(asignacones)
        db.session.commit()
        flash('Se a eliminado correctamente')
        return redirect(url_for('.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id ))
    else:
        return redirect(url_for('.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id )), 404

@brilado_completo.route('/emplado/<int:empleado_id>/trabajo/<int:trabajo_id>/serviciopieza/<int:serviciopieza_id>/servicio/<int:servicio_id>/vehiculo/<int:vehiculo_id>/editar', methods=['POST'])
@login_required
def update_asignacion(empleado_id, trabajo_id,serviciopieza_id,servicio_id, vehiculo_id):
    asignacones = Asignacion.query.filter_by(
                        empleado_id=empleado_id,
                        trabajo_id=trabajo_id,
                        serviciopieza_id=serviciopieza_id,
                        servicio_id=servicio_id, 
                        ).first()
    print(f'empleado_id: {empleado_id}')
    print(f'trabajo_id: {trabajo_id}')
    print(f'serviciopieza_id: {serviciopieza_id}')
    print(f'servicio_id: {servicio_id}')
    print(f'vehiculo: {vehiculo_id}')

    empleado = request.form.get('empleado')
    precio = request.form.get('car_precio')
    print(f'empleado: {empleado}')
    print(f'precio: {precio}')


    if asignacones:
        asignacones.empleado_id = empleado
        asignacones.trabajoprecio_id = precio
        db.session.commit()
        flash('Se a actualizado correctamente')
        return redirect(url_for('.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id ))
    else:
        return redirect(url_for('.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id )), 404


@brilado_completo.route('/pieza/precio', methods=['POST', 'GET'])
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