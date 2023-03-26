from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from flask_login import login_required

from src import db

from src.models.Pieza import Pieza, PiezaPrecio

from src.forms.pieza import PiezaForm

pieza = Blueprint('pieza', __name__, url_prefix='/pieza')

@pieza.route('/')
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
            p_precio = PiezaPrecio()
            
            id_pieza = request.form.get('id_pieza')
            precio = request.form.get('precio')

            if not id_pieza:
                flash('Debe selecionar una pieza')
                return redirect(url_for('pieza.index'))
            
            
            if not precio:
                flash('Debe ingresar el precio')
                return redirect(url_for('pieza.index'))
                

            query = PiezaPrecio.query.filter_by(id_piezas=id_pieza, pieza_precio=precio).first()

            if query:
                flash('Precio no disponible')
                return redirect(url_for('pieza.index'))


            p_precio.id_piezas = id_pieza
            p_precio.pieza_precio = precio
            
            db.session.add(p_precio)
            db.session.commit()
            
            flash('success, Creado con existo!')
            return redirect(url_for('pieza.index'))
        except Exception as e:
            print(e)
            flash('error')
            return redirect(url_for('pieza.index'))

@pieza.route('/delete/<int:id>', methods=['POST'])
def pieza_delete(id):
    pieza = Pieza.query.filter_by(id=id).first()
    try:
        if not pieza:
            flash("Error de servidor al intentar eliminar la pieza")
            return redirect(url_for('.index'))    
        
        pieza_precio = PiezaPrecio.query.filter_by(id_piezas=pieza.id).all()

        if pieza and not pieza_precio:
            db.session.delete(pieza)
            db.session.commit()
            flash('Pieza eliminada')
            return redirect(url_for('.index'))

        if pieza and pieza_precio:
            for item in pieza_precio:
                db.session.delete(item)
            db.session.delete(pieza)
            db.session.commit()
            flash('Pieza y Precios eliminados')
            return redirect(url_for('.index'))
    except Exception as e:
        print(e)
        flash('Error al itentar eliminar')
        return redirect(url_for('.index'))
    
@pieza.route('/delete/precio/<int:id>', methods=['POST'])
def precio_delete(id):
    pieza_precio = PiezaPrecio.query.filter_by(id=id).first()
    if not pieza_precio:
        flash("Error de servidor al intentar eliminar el precio")
        return redirect(url_for('.index'))    

    db.session.delete(pieza_precio)
    db.session.commit()
    flash('Precios eliminados')
    return redirect(url_for('.index'))
    
