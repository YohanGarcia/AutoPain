from flask import (
    jsonify, render_template, Blueprint, flash,
    redirect, request, session, url_for
)
from flask_login import login_required
from src import db
from src.heltper.formato import format_number
from src.models.Servicio import Servicio, Serviciolista,Serviciopago, Serviciopieza, Servicioprecio
from src.models.Vehiculo import Vehiculo
from src.models.Coche import Marca, Modelo
from src.models.Pieza import Pieza


from src.forms.vehiculoForm import VehiculoForm

from src.helper import current_date_format

vehiculo = Blueprint('vehiculo', __name__, url_prefix='/vehiculo')


@vehiculo.route('/create/cliente/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def vehiculo_create(cliente_id):
    vehiculo_forms = VehiculoForm()
    marcas = Marca.query.all()

    if request.method == 'POST' and vehiculo_forms.validate_on_submit:
        marca = int(request.form['car_brand'])
        modelo = int(request.form['car_models'])
        placa = vehiculo_forms.placa.data
        age = vehiculo_forms.age.data
        color = vehiculo_forms.color.data
        cliente_id = cliente_id

        nuevo_vehiculo = Vehiculo(
            marca_id=marca,
            modelo_id=modelo,
            cliente_id=cliente_id,
            placa=placa,
            age=age,
            color=color
        )
        flash('Vehiculo creado Exictosamente!.')

        db.session.add(nuevo_vehiculo)
        db.session.commit()
        return redirect(url_for('cliente.ver_cliente', cliente_id=cliente_id))
    return render_template('vehiculo/create.html', marcas=marcas, form=vehiculo_forms, current_date_format=current_date_format)

@vehiculo.route('/ver/<int:vehiculo_id>', methods=['GET', 'POST'])
@login_required
def get_vehiculo(vehiculo_id):
    vehiculo = Vehiculo.query.filter_by(id=vehiculo_id).first()
    servicio = Servicio.query.filter_by(vehiculo_id=vehiculo.id).all()
    serviciolista = Serviciolista.query.all() 
    piezas = Pieza.query.all()

    return render_template(
            'vehiculo/ver.html', 
            vehiculo=vehiculo, 
            servicios=servicio, 
            serviciolista=serviciolista, 
            piezas=piezas,
            cantidad_pieza=0,
            current_date_format=current_date_format,
            format_number=format_number,)

@vehiculo.route('/<int:vehiculo_id>/servicio-bono', methods=['POST'])
@login_required
def servicio_pago(vehiculo_id):
    cliente = request.form['cliente']
    servicio = request.form['servicio']
    bono = request.form['bono']
    descricion = request.form['descricion']
    print(f'Cliente: {cliente}', f'bono: {bono}', f'descricion: {descricion}', f'Servicio: {servicio}')

    save = Serviciopago(monto = bono,
                        descripcion=descricion,
                        cliente_id=cliente,
                        servicio_id=servicio)
    db.session.add(save)
    db.session.commit()
    flash('Enviado con exicto!')
    return redirect(url_for('.get_vehiculo',  vehiculo_id=vehiculo_id))

@vehiculo.route('/carbrand', methods=['POST', 'GET'])
def carbram():
    if request.method == 'POST':
        marca_id = request.form['marca_id']
        result = Modelo.query.filter_by(marca_id=marca_id).all()
        OutputArray = []
        for row in result:
            outputObj = {
                'id': row.id,
                'name': row.name
            }
            OutputArray.append(outputObj)
    return jsonify(OutputArray)


@vehiculo.route('/<int:vehiculo_id>/servicio/<int:servicio_id>', methods=['GET', 'POST'])
def delete_servicio(vehiculo_id, servicio_id):
    try:
        get_servicio = Servicio.query.filter_by(id=servicio_id).first()
       
        if get_servicio.serviciolistas:
            print('test 1')
            serviciolistas_id = get_servicio.serviciolistas
            db.session.delete(serviciolistas_id)
            print('Nombre del servicio eliminado')

        if get_servicio.serviciopagos:
            print('test 2')

            for serviciopago in get_servicio.serviciopagos:
                print('test 3')
                
                db.session.delete(serviciopago)
                print('Pagos del servicio eliminado')
        if get_servicio.servicioprecios:
            print('test 4')

            for precio_id_servicio in get_servicio.servicioprecios:
                print('test 5 1')
                print(precio_id_servicio)
                db.session.delete(precio_id_servicio)
            print('Precio eliminado')
        if get_servicio.serviciopiezas:
            print('test 5')
            for serviciopieza in get_servicio.serviciopiezas:
                if serviciopieza.pieza_precios:
                    print('test 6')
                    db.session.delete(serviciopieza.pieza_precios)
                    print('preio de pieza eliminado')
                print('Piezas eliminadas')
                db.session.delete(serviciopieza)
        if get_servicio.asignaciones:
            print('test 7')
            for asignaciones in get_servicio.asignaciones:
                print('test 8')
                db.session.delete(asignaciones)
                print('Aasignaciones eliminadas')

        print('test 9')
        print('test 10')
        db.session.delete(get_servicio)
        db.session.commit()
        print('test 11')
    except Exception as error:
        print( error)
    return redirect(url_for('.get_vehiculo', vehiculo_id=vehiculo_id))