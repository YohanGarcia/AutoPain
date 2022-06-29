from flask import(
    render_template, Blueprint, flash, redirect, request, url_for
)

from src.models.Cliente import Cliente
from src.models.Vehiculo import Vehiculo


from flask_login import current_user, login_required

from src import db

from src.forms.cliente_form import ClienteForm

cliente = Blueprint('cliente', __name__, url_prefix='/cliente')

@cliente.route('/')
@login_required
def index():
    cliente = Cliente.query.filter_by(user_id=current_user.id).all()
    db.session.commit()
    return render_template('cliente/index.html', clientes=cliente)

@cliente.route('/<int:id>')
@login_required
def get_cliente(id):
    cliente = Cliente.query.filter_by(id=id).first()
    vehiculo = Vehiculo.query.filter_by(cliente_id=id).all()
    
    if cliente:
        if current_user.id == cliente.user_id:
        
            return render_template('cliente/vercliente.html', cliente=cliente, vehiculos=vehiculo)
    
    return render_template('home/page-404.html'), 404
    

#Registrar usuarios
@cliente.route('/create', methods=['GET','POST'])
@login_required
def add_cliente():
    form = ClienteForm()

    if request.method == 'POST':
        if form.validate_on_submit:

            username = form.username.data
            lastname = form.lastname.data
            telefono = form.telefono.data

            nuevo_cliente = Cliente(username, lastname, telefono, current_user.id)
            
            error = None
            if not username:
                error = 'Se requiere nombre de usuario'
            elif not lastname:
                error = 'Se requiere el apallido'
            elif not telefono:
                error = 'Se requiere el Numero de telefono'
            
            cliente_name = Cliente.query.filter_by(username=username).first()
            if cliente_name == None:
                db.session.add(nuevo_cliente)
                db.session.commit()
                flash('Cliente Registrado exictosa mente')
                return redirect(url_for('index.index'))
            else:
                error = f'Este cliente {username} exicte '
            flash(error) 
        
    return render_template('cliente/create.html', form=form)
