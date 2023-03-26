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
def index():
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
            return redirect(url_for('.index'))
        marca = Marca(name=marca_forms.name.data)
        db.session.add(marca)
        db.session.commit()
        flash('Marca registrada exitosamente!.')
        return redirect(url_for('.index'))
    return redirect(url_for('.index'))
    

@coche.route('/modelo', methods=['POST'])
@login_required
def modelo():
    if request.method == 'POST':
        name = request.form.get('name')
        marca_id = request.form.get('marca')

        get_modelo = Modelo.query.filter_by(name=name, marca_id=marca_id).first()
        if get_modelo:
            flash('El Coche ya exicte!.')
            return redirect(url_for('.index'))
        get_name = Modelo.query.filter_by(name=name).first()
        if get_name:
            flash('El Modelo ya exicte!.')
            return redirect(url_for('.index'))        

        modelo = Modelo(name, marca_id)
        db.session.add(modelo)
        db.session.commit()
        flash('Modelo registrada exitosamente!.')
        return redirect(url_for('.index'))
    return redirect(url_for('.index'))

@coche.route('/delete/<int:id>', methods=['POST'])
def marca_delete(id):
    marca = Marca.query.filter_by(id=id).first()
    try:    
        if not marca:
            flash("Error de servidor al intentar eliminar la Marca")
            return redirect(url_for('.index'))    
        
        marca_modelo = Modelo.query.filter_by(marca_id=marca.id).all()

        if marca and not marca_modelo:
            db.session.delete(marca)
            db.session.commit()
            flash('Marca eliminada')
            return redirect(url_for('.index'))

        if marca and marca_modelo:
            for item in marca_modelo:
                db.session.delete(item)
            db.session.delete(marca)
            db.session.commit()
            flash('Marca y Modelos eliminados')
            return redirect(url_for('.index'))
    except Exception as e:
        print(e)
        flash('Error al itentar eliminar')
        return redirect(url_for('.index'))

@coche.route('/delete/modelo/<int:id>', methods=['POST'])
def modelo_delete(id):
    query_modelo = Modelo.query.filter_by(id=id).first()
    if not query_modelo:
        flash("Error de servidor al intentar eliminar")
        return redirect(url_for('.index'))    

    db.session.delete(query_modelo)
    db.session.commit()
    flash('Modelo eliminado')
    return redirect(url_for('.index'))