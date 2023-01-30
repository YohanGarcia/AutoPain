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
        precio = request.form.get('precio')
        trabajo = request.form.get('trabajo')

        save = TrabajoPrecio(precio=precio, trabajo_id=trabajo)
        db.session.add(save)
        db.session.commit()
        flash('Registrada exitoso!.')
        return redirect(url_for('trabajo.index'))
    return redirect(url_for('trabajo.index'))
    