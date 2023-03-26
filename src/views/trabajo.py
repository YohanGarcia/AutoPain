from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from flask_login import login_required

from src import db

from src.models.Trabajos import Trabajo, TrabajoPrecio

from src.forms.pieza import PiezaForm

trabajo = Blueprint('trabajo', __name__, url_prefix='/trabajo')

@trabajo.route('')
@login_required
def index():
    trabajos = Trabajo.query.all()
    return render_template('/trabajo/index.html', trabajos=trabajos)

@trabajo.route('/create', methods=['POST'])
@login_required
def trabajo_create():
    if request.method == 'POST':
        name = request.form.get('name')
        trabajo = Trabajo.query.filter_by(name=name).first()
        if trabajo:
            flash('Error, El tipo de trabajo ya exicte!.')
            return redirect(url_for('trabajo.index'))
        else:
            save = Trabajo(name=name)
            db.session.add(save)
            db.session.commit()
            flash('registro con exicto!.')
            return redirect(url_for('trabajo.index'))
    return redirect(url_for('trabajo.index'))

@trabajo.route('/precio', methods=['POST'])
@login_required
def precio():
    if request.method == 'POST':
        try:
            t_precio = TrabajoPrecio()

            precio = request.form.get('precio')
            trabajo = int(request.form.get('trabajo'))

            get_precio = TrabajoPrecio.query.filter_by(trabajo_id=trabajo, precio=precio).first()


            if not trabajo:
                flash('Debe selecionar una trabajo')
                return redirect(url_for('trabajo.index'))
    
            if get_precio:
                flash('Precio no disponible')
                return redirect(url_for('trabajo.index'))

            t_precio.precio = precio
            t_precio.trabajo_id = trabajo

            db.session.add(t_precio)
            db.session.commit()
            flash('Registrada exitoso!.')
            return redirect(url_for('trabajo.index'))
        except Exception as e:
            print(e)
            flash('Error al intentar registrar los datos enviado')
            return redirect(url_for('trabajo.index'))


@trabajo.route('/delete/<int:id>', methods=['POST'])
def trabajo_delete(id):
    query_trabajo = Trabajo.query.filter_by(id=id).first()
    try:
        if not query_trabajo:
            flash("Error de servidor al intentar eliminar la query_trabajo")
            return redirect(url_for('trabajo.index'))    
        
        trabajo_precio = TrabajoPrecio.query.filter_by(trabajo_id=query_trabajo.id).all()

        if query_trabajo and not trabajo_precio:
            db.session.delete(query_trabajo)
            db.session.commit()
            flash('Nombre de trabajo eliminada')
            return redirect(url_for('trabajo.index'))

        if query_trabajo and trabajo_precio:
            for iten in trabajo_precio:
                db.session.delete(iten)
            db.session.delete(query_trabajo)
            db.session.commit()
            flash('trabajo y Precios eliminados')
            return redirect(url_for('trabajo.index'))
    except Exception as e:
        print(e)
        flash('Error al itentar eliminar')
        return redirect(url_for('.index'))

@trabajo.route('/delete/precio/<int:id>', methods=['POST'])
def precio_delete(id):
    trabajo_precio = TrabajoPrecio.query.filter_by(id=id).first()
    if not trabajo_precio:
        flash("Error de servidor al intentar eliminar el precio")
        return redirect(url_for('trabajo.index'))    

    db.session.delete(trabajo_precio)
    db.session.commit()
    flash('Precios eliminados')
    return redirect(url_for('trabajo.index'))



        
    