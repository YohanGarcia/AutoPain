from flask import render_template, Blueprint, redirect, request, url_for

from flask_login import login_required

from src import db

from src.models.Piesa import Piesa, Precio
from src.forms.piesa_form import PiesaForm, PrecioForm

piesa = Blueprint('piesa', __name__, url_prefix='/piesa')

@piesa.route('', methods=['GET', 'POST'])
@piesa.route('/precio', methods=['GET', 'POST'])
@piesa.route('/piesa', methods=['GET', 'POST'])
@login_required
def main():
    form = PiesaForm()
    get_piesa = Piesa.query.all()
    if request.path == '/piesa/piesa':

        if request.method == 'POST':
            if form.validate_on_submit:
                name = form.name.data
                print(name)
                nueva_piesa = Piesa(name)
                db.session.add(nueva_piesa)
                db.session.commit()
                return redirect(url_for('piesa.main'))

    if request.path == '/piesa/precio':
        if request.method == 'POST':
            piesa_id = int(request.form.get('piesa'))
            precio = int(request.form.get('precio'))
            print(type(piesa_id))
            print(type(precio))
            nuevo_precio = Precio(precio, piesa_id)
            db.session.add(nuevo_precio)
            db.session.commit()
            return redirect(url_for('piesa.main'))
    return render_template('piesa/piesacreate.html', form=form, piesas=get_piesa)


    
    
    
            