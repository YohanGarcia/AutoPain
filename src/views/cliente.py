from flask import(
    render_template, Blueprint, flash, redirect, request, url_for, session
)
from flask_login import login_required

from src.models.Cliente import Cliente
from src.models.Vehiculo import Vehiculo

from src import db

from src.forms.cliente import ClienteForm

from src.helper import current_date_format

cliente = Blueprint('cliente', __name__, url_prefix='/cliente')


def paginate(query, page=1, per_page=10):
    """
    Retorna una instancia de paginación de los resultados de una consulta
    """
    return query.paginate(page=page, per_page=per_page)


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
    per_page = request.args.get('per_page', 6, type=int)
 
    clientes_query = Cliente.query.order_by(Cliente.username.desc())

    # Paginar los resultados
    paginated_users = paginate(clientes_query, page, per_page)

    return render_template('/cliente/index.html', clientes=paginated_users, current_date_format=current_date_format)

@cliente.route('/ver/<int:cliente_id>')
@login_required
def ver_cliente(cliente_id):
    clientes = Cliente.query.filter_by(id=cliente_id).first()
    return render_template('/cliente/ver.html', cliente=clientes, current_date_format=current_date_format)

@cliente.route('/delete/<int:id>', methods=['POST'])
def cliente_delete(id):
    cliente = Cliente.query.filter_by(id=id).first()
    cliente_vehiculo = Vehiculo.query.filter_by(cliente_id=cliente.id).all()
    try:
        if not cliente:
            flash("Error de servidor al intentar eliminar el cliente")
            return redirect(url_for('.cliente_all'))    

        if cliente and not cliente_vehiculo:
            db.session.delete(cliente)
            db.session.commit()
            flash('Cliente eliminada')
            return redirect(url_for('.cliente_all'))

        if cliente and cliente_vehiculo:
            for vehiculo in cliente_vehiculo:       
                db.session.delete(vehiculo)
            db.session.delete(cliente)
            db.session.commit()
            print(f'Se elimino el cliente {cliente.username} y el vehoculo')
            flash('Pieza y Precios eliminados')
            return redirect(url_for('.cliente_all'))
    except Exception as e:
        print(e)
        flash('Error al itentar eliminar')
        return redirect(url_for('.cliente_all'))
    
@cliente.route('/vehiculo/delete/<int:id>/<int:clinte_id>', methods=['POST'])
def cliente_vehiculo_delete(id,clinte_id):
    cliente_vehiculo = Vehiculo.query.filter_by(id=id).first()
    try:
        if not cliente_vehiculo:
            flash("Error de servidor al intentar eliminar el vehiculo")
            return redirect(url_for('.ver_cliente', cliente_id=clinte_id))    

        db.session.delete(cliente_vehiculo)
        db.session.commit()
        flash('Vehiculos eliminados')
        return redirect(url_for('.ver_cliente', cliente_id=clinte_id))
    except Exception as e:
        print(e)
        flash('Error al itentar eliminar')
        return redirect(url_for('.ver_cliente', cliente_id=clinte_id))
    