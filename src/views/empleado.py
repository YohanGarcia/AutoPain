from fileinput import filename
from flask import (
    render_template, Blueprint, flash,
    redirect, request, url_for
)
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from prettytable import PrettyTable

from src import db, allowed_file, app
from src.helper import current_date_format
from src.heltper.empleado_total import Empleado_total
from src.heltper.enumerate_pieza import enumerate_serviciopiezas
from src.heltper.formato import format_number
from src.models.Servicio import Servicio, Serviciopieza
from src.models.Vehiculo import Vehiculo
from src.models.Empleados import Empleado
from src.models.Asignacion import Asignacion

empleado = Blueprint('empleado', __name__, url_prefix='/empleado')


@empleado.route('create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            lastname = request.form.get('lastname')
            telefono = request.form.get('telefono')
            telefonocasa = request.form.get('telefonocasa')
            correo = request.form.get('correo')
            nacimiento = request.form.get('nacimiento')
            cedula = request.form.get('cedula')
            foto = request.files['foto']
         
            filename = secure_filename(foto.filename)
            
            nuevo_empleado = Empleado(
                name=name,
                lastname=lastname,
                telefono=telefono,
                telefonocasa=telefonocasa,
                cedula=cedula,
                correo=correo,
                foto=filename,
                nacimiento=nacimiento,
            )
            db.session.add(nuevo_empleado)
            db.session.commit()
            flash('Empleado registrado con exicto!.')
            if foto and allowed_file(filename):
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('empleado.create'))
        except Exception as e:
            print(e)
            flash('Error creating hay datos que pertesen a otro usuario')
    return render_template('empleado/created.html')


# @empleado.route('/ver/<int:id>', methods=['GET', 'POST'])
# @login_required
# def ver(id):
#     empleado = Empleado.query.filter_by(id=id).first()
#     asignacion = Asignacion.query.filter_by(empleado_id=empleado.id).all()

#     serviciopiezas = []

#     for i in asignacion:
#         servicios = Servicio.query.filter_by(id=i.id).all()

#         for item in servicios:
#             asignaciones = [asignacion for asignacion in item.asignaciones if asignacion.empleado_id == id]

#             if asignaciones:
#                 print('paso el if asignaciones')
#                 serviciopiezas.append({
#                     'datos': [{
#                         'id': item.id,
#                         'pieza': [pieza.piezas.name for pieza in item.serviciopiezas],
#                         "asignaciones": asignaciones
#                     }]
#                 })
#     for item in serviciopiezas:
#         for datos in item['datos']:
#             print(f"ID: {datos['id']}")
#             print("Piezas: ")
#             for pieza in datos['pieza']:
#                 print(f"- {pieza}")
#             print("Asignaciones:")
#             for asignacion in datos['asignaciones']:
#                 print(f"- {asignacion.id}: {asignacion.empleados.name}")
#             print("\n")


#     return render_template('empleado/trabajos.html',
#                            empleado=empleado,
#                            current_date_format=current_date_format,
#                            serviciopiezas=serviciopiezas,
#                            format_number=format_number,
#                            )

@empleado.route('/ver/<int:id>', methods=['GET', 'POST'])
@login_required
def ver(id):
    empleado = Empleado.query.filter_by(id=id).first()
    asignaciones = Asignacion.query.filter_by(empleado_id=empleado.id).all()

# Filtrar todas las asignaciones del empleado
    asignaciones_ids = [a.id for a in asignaciones]

    datos_piezas = []

    # Recorrer todos los servicios
    for servicio in Servicio.query.all():
        # Filtrar solo los Serviciopieza con asignaciones del empleado
        serviciopiezas = [sp for sp in servicio.serviciopiezas if sp.asignaciones and sp.asignaciones[0].id in asignaciones_ids]

        # Si hay Serviciopiezas para este Servicio, agregar a la lista
        if serviciopiezas:
            # Recorrer todas las Serviciopiezas
            for sp in serviciopiezas:
                # Crear una lista de asignaciones correspondientes a las piezas de la Serviciopieza
                asignaciones_piezas = [a for a in asignaciones if a.id == sp.asignaciones[0].id]

                datos_piezas.append({
                    'datos': [{
                        'id': servicio.id,
                        'pieza': {
                            'name': sp.piezas.name,
                            'asignaciones': asignaciones_piezas
                        }
                    }]
                })

    print(datos_piezas)
    # Crear la tabla
    table = PrettyTable()
    table.field_names = ['ID', 'Pieza', 'Asignaciones']

    # Agregar los datos a la tabla
    for datos in datos_piezas:
        if 'id' in datos:
            table.add_row([datos['id'], datos['pieza'], datos['asignaciones']])
        else:
    # Manejar el caso en el que la clave 'id' no está presente en el diccionario
            print("La clave 'id' no está presente en el diccionario.")

    # Imprimir la tabla
    print(table)
    
    return render_template('empleado/trabajos.html',
                           empleado=empleado,
                           current_date_format=current_date_format,
                           datos_piezas=datos_piezas,
                           format_number=format_number)