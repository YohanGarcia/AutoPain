from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from flask_login import login_required

from src import db

from src.models.Coche import Marca, Modelo
from src.forms.coche import MarcaForm

coche = Blueprint('coche', __name__, url_prefix='/coche')


@coche.route('/')
@login_required
def coche_all():
    marcas = Marca.query.all()
    marca_forms = MarcaForm(request.form)

    return render_template('/coche/coche.html', marcas=marcas, form=marca_forms)

@coche.route('/marca', methods=['GET','POST'])
@login_required
def marca():
    marca_forms = MarcaForm(request.form)
    if request.method == 'POST' and marca_forms.validate():
        get_marca = Marca.query.filter_by(name=marca_forms.name.data).first()
        if get_marca:
            flash('La marca ya exicte!.')
            return redirect(url_for('coche.coche_all'))
        marca = Marca(name=marca_forms.name.data)
        db.session.add(marca)
        db.session.commit()
        flash('Marca registrada exitosamente!.')
        return redirect(url_for('coche.coche_all'))
    return redirect(url_for('coche.coche_all'))
    

@coche.route('/modelo', methods=['POST'])
@login_required
def modelo():
    if request.method == 'POST':
        name = request.form.get('name')
        marca_id = request.form.get('marca')

        get_modelo = Modelo.query.filter_by(name=name, marca_id=marca_id).first()
        if get_modelo:
            flash('El Coche ya exicte!.')
            return redirect(url_for('coche.coche_all'))
        get_name = Modelo.query.filter_by(name=name).first()
        if get_name:
            flash('El Modelo ya exicte!.')
            return redirect(url_for('coche.coche_all'))        

        modelo = Modelo(name, marca_id)
        db.session.add(modelo)
        db.session.commit()
        flash('Modelo registrada exitosamente!.')
        return redirect(url_for('coche.coche_all'))
    return redirect(url_for('coche.coche_all'))

