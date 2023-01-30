from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from flask_login import login_required

from src import db

from src.models.Pieza import Pieza, PiezaPrecio

from src.forms.pieza import PiezaForm

pieza = Blueprint('pieza', __name__, url_prefix='/pieza')

@pieza.route('')
@login_required
def index():
    piezas = Pieza.query.all()

    form = PiezaForm(request.form)
    return render_template('/pieza/pieza.html', piezas=piezas, form=form)

@pieza.route('/create', methods=['POST'])
@login_required
def pieza_create():
    form = PiezaForm(request.form)
    if request.method == 'POST' and form.validate():
        pieza = Pieza.query.filter_by(name=form.name.data).first()
        if pieza:
            flash('Error, La pieza ya exicte!.')
            return redirect(url_for('pieza.index'))
        else:
            save = Pieza(name=form.name.data)
            db.session.add(save)
            db.session.commit()
            flash('Pieza registrada con exicto!.')
            return redirect(url_for('pieza.index'))
    return redirect(url_for('pieza.index'))
    
@pieza.route('/precio', methods=['POST'])
@login_required
def precio():
    if request.method == 'POST':
        try:
            pieza = PiezaPrecio()
            
            id_pieza = request.form.get('id_pieza')
            precio = request.form.get('precio')
            print('pieza id: ', id_pieza)
            print('precio: ', precio)
            pieza.id_piezas = id_pieza
            pieza.pieza_precio = precio
            
            db.session.add(pieza)
            db.session.commit()
            
            print(f'pieza: {id_pieza}, precio: {precio}')
            flash('success, Creado con existo!')
            return redirect(url_for('pieza.index'))
        except Exception as e:
            print(e)
            flash('error')
            return redirect(url_for('pieza.index'))