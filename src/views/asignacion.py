from flask import (
    jsonify, render_template, Blueprint, flash,
    redirect, request, url_for
)

from src import db
from src.heltper.editar_asignacion_empleado import Editar_asignacion_empleado
from src.heltper.eliminar_asinacion_empleado import Eliminar_asignacion_empleado
from src.heltper.Eliminar_servicio_pieza import Eliminar_servicio_pieza
from src.models.Asignacion import Asignacion
from src.models.Servicio import Serviciopieza
from src.models.Trabajos import Trabajo, TrabajoPrecio

asignacion = Blueprint('asignacion', __name__, url_prefix='/asignacion')


@asignacion.route('/<int:serviciopieza_id>/servicio/<int:servicio_id>')
def index(serviciopieza_id, servicio_id):
    asignacionpieza = Asignacion.query.filter_by(
        serviciopieza_id=serviciopieza_id, servicio_id=servicio_id).first()
    asignacionpiezas = Asignacion.query.filter_by(
        serviciopieza_id=serviciopieza_id, servicio_id=servicio_id).all()

    return render_template('/servicios/asignacion.html', asignacionpiezas=asignacionpiezas, asignacionpieza=asignacionpieza)


@asignacion.route('/<int:servicio_id>/vehiculo/<int:vehiculo_id>/asignacion1', methods=['GET', 'POST'])
def asignacion1(servicio_id, vehiculo_id):
    if request.method == 'POST':
        piezas = Serviciopieza.query.filter_by(servicio_id=servicio_id).all()
        empleado = request.form.get('empleado')
        precio = request.form.get('precio')
        trabajo = request.form.get('trabajo')
        print(precio, 'precio provando')
        if not empleado:
            flash('Selecione un empleado')
            return redirect(url_for('servicio.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))

        if not precio:
            flash('Ingrese el precio')
            return redirect(url_for('servicio.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))

        if not trabajo:
            flash('Selecione un tipo de trabajo')
            return redirect(url_for('servicio.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))

        else:
            for pieza in piezas:
                save = Asignacion(serviciopieza_id=pieza.id, trabajo_id=trabajo,
                                  empleado_id=empleado, precio=precio, servicio_id=servicio_id)
                # db.session.add(save)
                # db.session.commit()
            flash('Registrado exictosamente!.')
    return redirect(url_for('pintura-general.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))


@asignacion.route('/<int:servicio_id>/vehiculo/<int:vehiculo_id>/asignacion2', methods=['GET', 'POST'])
def asignacion2(servicio_id, vehiculo_id):
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
    return redirect(url_for('pintura-general.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))


@asignacion.route('/<int:servicio_id>/vehiculo/<int:vehiculo_id>/asignacion3', methods=['GET', 'POST'])
def asignacion_brillado_general(servicio_id, vehiculo_id):
    print('entrada 1')
    if request.method == 'POST':
        print('entrada 2')
        id_pieza = request.form.get('id_pieza')
        empleado = request.form.get('empleado')
        trabajo = request.form.get('car_trabajo')
        precio = request.form.get('car_precio')

        print(f'pieza id: {id_pieza}')
        print(f'empleado: {empleado}')
        print(f'car_trabajo: {trabajo}')
        print(f'precio: {precio}')

        if not empleado:
            flash('Selecione un empleado')
        if not precio:
            flash('Ingrese el precio')
        if not trabajo:
            flash('Selecione un tipo de trabajo')

        else:
            save = Asignacion(serviciopieza_id=id_pieza,
                                trabajo_id=trabajo,
                                empleado_id=empleado,
                                trabajoprecio_id=precio,
                                servicio_id=servicio_id)
            db.session.add(save)
            db.session.commit()
            flash('Registrado exictosamente!.')
    return redirect(url_for('brillado-completo.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))

@asignacion.route('/<int:serviciopieza_id>/<int:servicio_id>/vehiculo/<int:vehiculo_id>', methods=['GET','POST'])
def cambiar_asignacion(servicio_id,vehiculo_id,serviciopieza_id):
    asigncion_cambiar = Asignacion.query.filter_by(serviciopieza_id=serviciopieza_id).first()
    if not asigncion_cambiar:
        print('Error no encontro esa informacion')
    else:
        if request.method == 'POST':
            empleado = request.form.get('empleado')
            precio = request.form.get('precio')
            
    
            if not empleado:
                flash('selecione un empleado')
            elif not precio:
                flash('Ingrese el precio')
            else:
                asigncion_cambiar.empleado_id = empleado
                asigncion_cambiar.precio = precio
                db.session.commit()
                flash('Cambio exictoso!')
    return redirect(url_for('pintura-general.index', vehiculo_id=vehiculo_id,servicio_id=servicio_id))


@asignacion.route('/trabajoprecio', methods=['POST', 'GET'])
def carbram():

    if request.method == 'POST':
        trabajo_id = request.form['trabajo_id']
        result = TrabajoPrecio.query.filter_by(trabajo_id=trabajo_id).all()
        OutputArray = []
        for row in result:
            outputObj = {
                'id': row.id,
                'precio': row.precio
            }
            OutputArray.append(outputObj)
    return jsonify(OutputArray)



@asignacion.route('/delete/asignacion/<int:asignacion_id>', methods=['POST'])
def delete_asignacion(asignacion_id):
    ruta = request.form.get('ruta')
    return Eliminar_asignacion_empleado(id=asignacion_id, ruta=ruta)

@asignacion.route('/update/asignacion/<int:asignacion_id>', methods=['POST'])
def update_asignacion(asignacion_id):
    empleado = request.form.get('empleado')
    precio = request.form.get('car_precio')
    ruta = request.form.get('ruta')
    return Editar_asignacion_empleado(id=asignacion_id, precio=precio,empleado=empleado, ruta=ruta)

@asignacion.route('/delete/pieza/<int:asignacion_id>', methods=['POST'])
def delete_sevicio_pieza(asignacion_id):
    ruta = request.form.get('ruta')
    return Eliminar_servicio_pieza(id=asignacion_id, ruta=ruta)