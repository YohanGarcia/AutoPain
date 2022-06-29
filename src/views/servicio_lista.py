from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from flask_login import login_required

from src import db

from src.models.servicios import Lista
from src.forms.lista_form import ListaForm

lista = Blueprint('lista', __name__, url_prefix='/lista')

@lista.route('', methods=['GET', 'POST'])
@login_required
def main():
    form = ListaForm()
    query = Lista.query.all()
    if request.method == 'POST' and form.validate_on_submit:
        name = form.name.data
        print(name)
        nueva_lista = Lista(name)
        db.session.add(nueva_lista)
        db.session.commit()
        return redirect(url_for('lista.main'))
    return render_template('servicios/lista.html', form=form, lista=query)