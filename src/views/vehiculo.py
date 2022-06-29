import json
from turtle import color
from flask import(
    jsonify, render_template, Blueprint, flash, 
    redirect, request, session, url_for
)
from flask_login import current_user, login_required

from src import db


from src.models.Vehiculo import Vehiculo
from src.models.Cliente import Cliente
from src.models.Coche import Marca, Modelo
from src.models.servicios import Lista, Servicio

from src.forms.vehiculoForm import VehiculoForm
vehiculo = Blueprint('vehiculo', __name__, url_prefix='/vehiculo')

@vehiculo.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def main(id):
    form = VehiculoForm()
    marcas = Marca.query.all()
    msg = ''

    if request.method == 'POST':

        if form.validate_on_submit:
            marca = int(request.form['car_brand'])
            modelo = int(request.form['car_models'])
            placa = form.placa.data
            age = form.age.data
            color = form.color.data
            cliente_id = id
            print([marca,modelo,placa,age,color,cliente_id,current_user.id])

            coche = Vehiculo.query.filter(
                    (Vehiculo.marca_id==marca) & (Vehiculo.modelo_id==modelo) &
                    (Vehiculo.cliente_id==cliente_id) & (Vehiculo.user_id==current_user.id) &
                    (Vehiculo.placa == placa)
                    ).first()

            cliente = Cliente.query.filter_by(id=cliente_id).first()
            
            nuevo_vehiculo = Vehiculo(
                marca,
                modelo,
                cliente_id,
                current_user.id,
                placa,
                age,
                color
            )
            
            
            db.session.add(nuevo_vehiculo)
            db.session.commit()
            return redirect(url_for('index.index'))

    return render_template('vehiculo/create.html', marcas=marcas, form=form, msg=msg)

@vehiculo.route('/ver/<int:id>', methods=['GET', 'POST'])
@login_required
def get_vehiculo(id):
    query = Vehiculo.query.filter_by(id=id).first()
    lista = Lista.query.all()
    if request.method == "POST":
        name = request.form.get('name')
        nuevo_servicio = Servicio(lista_id=int(name), vehiculo_id=id, user_id=current_user.id)
        db.session.add(nuevo_servicio)
        db.session.commit()
        return redirect(f'/vehiculo/ver/{id}')
    return render_template('vehiculo/ver.html', query=query, listas=lista)

@vehiculo.route('/carbrand', methods=['GET', 'POST'])
@login_required
def carbram():
    if request.method == 'POST':
        marca_id = request.form['marca_id']
        print(marca_id)
        result = Modelo.query.filter_by(marca_id=marca_id).all()
        OutputArray = []
        for row in result:
            outputObj = {
                'id': row.id,
                'name': row.name
            }
            OutputArray.append(outputObj)
    return jsonify(OutputArray)