from flask import (
    jsonify, render_template, Blueprint, flash,
    redirect, request, url_for
)

from flask_login import login_required
from src import db
from src.helper import current_date_format
from src.heltper.editar_asignacion_empleado import Editar_asignacion_empleado
from src.heltper.eliminar_asinacion_empleado import Eliminar_asignacion_empleado
from src.heltper.empleado_total import Empleado_total
from src.heltper.formato import format_number
from src.models.Productos import HistorialVentas, Producto

from src.models.Servicio import Servicio, Serviciolista, Servicioprecio, Serviciopieza
from src.models.Vehiculo import Vehiculo
from src.models.Pieza import Pieza, PiezaPrecio
from src.models.Asignacion import Asignacion
from src.models.Empleados import Empleado
from src.models.Trabajos import Trabajo, TrabajoPrecio

pinturaGeneral = Blueprint('pintura-general', __name__,
                           url_prefix='/pintura/general')
@pinturaGeneral.route('/servicios/<int:servicio_id>/vehiculo/<int:vehiculo_id>', methods=['GET', 'POST'])
@login_required
def index(servicio_id, vehiculo_id):
    vehiculo = Vehiculo.query.filter_by(id=vehiculo_id).first()
    servicio = Servicio.query.filter_by(id=servicio_id).first()
    serviciopiezas = Serviciopieza.query.filter_by(servicio_id=servicio_id).all()
    asignaciones = Asignacion.query.filter_by(servicio_id=servicio_id).all()
    venta = HistorialVentas.query.filter_by(status=True, id_servicios=servicio_id, id_vehiculos=vehiculo_id).all()
    query_productos = Producto.query.filter_by(status=True).all()
    piezas = Pieza.query.all()
   
    empleados = Empleado.query.all()
    trabajos = Trabajo.query.all()

    ruta = request.path

    counter = 0
    for precio in servicio.servicioprecios:
        if precio.precio is not None:
            counter += precio.precio
    
    return render_template(
        '/servicios/pintura-general.html',
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
        ruta=ruta,
        empleados_total=Empleado_total(asignaciones),
        format_number=format_number,
        current_date_format=current_date_format
    )




@pinturaGeneral.route('/pieza/precio', methods=['POST', 'GET'])
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