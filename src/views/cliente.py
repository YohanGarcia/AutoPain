from flask import(
    render_template, Blueprint, flash, redirect, request, url_for, session
)
from flask_login import login_required

from src.models.Cliente import Cliente

from src import db

from src.forms.cliente import ClienteForm

from src.helper import current_date_format

cliente = Blueprint('cliente', __name__, url_prefix='/cliente')

#Registrar usuarios
@cliente.route('/create', methods=['GET', 'POST'])
@login_required
def cliente_create():
    cliente_forms = ClienteForm(request.form)
    print('entro aqui 1')
    if request.method == 'POST':
        print('entro aqui 2')
        
        cliente = Cliente.query.filter_by(username=cliente_forms.username.data,
                                            lastname=cliente_forms.lestname.data).first()
        if cliente:
            print('entro aqui 3')
        
            flash('El Clinete exicte en la base de datos, No se puede repiter')
            return redirect(url_for('cliente.cliente_create'))

        try:
            print('entro aqui 4')
            
            save = Cliente(username=cliente_forms.username.data,
                        lastname=cliente_forms.lestname.data,
                        telefono=request.form.get('telefono'),
                        cedula=cliente_forms.cedula.data,
                        direccion=cliente_forms.direccion.data)
            db.session.add(save)
            db.session.commit() 
            flash('Cliente registrado')
            return redirect(url_for('cliente.cliente_all'))
        except Exception as e:
            print(e)       
            flash('Error de servidor')
            return redirect(url_for('cliente.cliente_all'))
    return render_template('/cliente/create.html', form=cliente_forms)

@cliente.route('', methods=['GET'])
@login_required
def cliente_all():
    page = request.args.get('page', 1, type=int)
 
    clientes = Cliente.query.filter().order_by(Cliente.username,
        Cliente.lastname,
        Cliente.telefono).paginate(page=page, per_page=5)
    return render_template('/cliente/index.html', clientes=clientes, current_date_format=current_date_format)

@cliente.route('/ver/<int:cliente_id>')
@login_required
def ver_cliente(cliente_id):
    clientes = Cliente.query.filter_by(id=cliente_id).first()
    return render_template('/cliente/ver.html', cliente=clientes, current_date_format=current_date_format)
