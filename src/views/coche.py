from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from flask_login import login_required

from src import db

from src.models.Coche import Marca, Modelo
from src.forms.coche_form import MarcaForm, ModeloForm

coche = Blueprint('coche', __name__, url_prefix='/coche')

@coche.route('/', methods=['GET', 'POST'])
@coche.route('/marca', methods=['GET', 'POST'])
@coche.route('/modelo', methods=['GET', 'POST'])
@login_required
def marca():
    form = MarcaForm()
    get_marca = Marca.query.order_by(Marca.name)
    if request.path == '/coche/marca':
        if request.method == 'POST':
                name = form.name.data
                nueva_marca = Marca(name)

                marca = Marca.query.filter_by(name=name).first()
                if marca:
                    return redirect(url_for('coche.marca', form=form, msg=f'la {marca.name} ya exicte'))
                db.session.add(nueva_marca)
                db.session.commit()
                return redirect(url_for('coche.marca'))

    if request.path == '/coche/modelo':
        if request.method == 'POST':
            name = request.form.get('name')
            marca_id = request.form.get('marca')

            modelo = Modelo.query.filter_by(name=name).first()
            nuevo_modelo = Modelo(name, marca_id)
            if modelo:
                return render_template('coche/cochecreate.html',marcas=get_marca, form=form, msg=f'El modelo de coche {modelo.name} ya exicte')
            db.session.add(nuevo_modelo)
            db.session.commit()
            return redirect(url_for('coche.marca'))
    return render_template('coche/cochecreate.html', form=form, marcas=get_marca)

