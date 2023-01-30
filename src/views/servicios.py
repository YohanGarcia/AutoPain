from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from collections import Counter

from flask_login import login_required
from src import db
from src.forms.serviciolista import ServicioListaForm

from src.models.Servicio import Servicio, Serviciolista, Servicioprecio, Serviciopieza
from src.models.Vehiculo import Vehiculo
from src.models.Pieza import Pieza
from src.models.Asignacion import Asignacion
from src.models.Empleados import Empleado
from src.models.Trabajos import Trabajo, TrabajoPrecio

servicio = Blueprint('servicio', __name__, url_prefix='/servicio')

@servicio.route('/<int:servicio_id>/vehiculo/<int:vehiculo_id>', methods=['GET','POST'])
@login_required
def index(servicio_id, vehiculo_id):
    vehiculo = Vehiculo.query.filter_by(id=vehiculo_id).first()
    servicio = Servicio.query.filter_by(id=servicio_id).first()
    serviciopiezas = Serviciopieza.query.filter_by(servicio_id=servicio_id).all()
    asignacion = Asignacion.query.filter_by(servicio_id=servicio_id).all()
    
    trabajoprecio= []
    for item in asignacion:
        if item.trabajoprecio_id:
            a = item.trabajoprecio_id
            trabajoprecio.append(a)
    d = []
    for emp in asignacion:
        e = emp.empleado_id
        d.append(e)
    c = Counter(d)
    employe = max(c, key=c.get) if c else None
    empleado = Asignacion.query.filter_by(servicio_id=servicio_id,empleado_id=employe).first()
    # pre = 0
    # for item2 in empleado:
    #     print(item2.empleados.name)
    #     if item2.precio:
    #         print(item2.precio)
    #         pre += int(item2.precio)
    # print(pre)
    piezas = Pieza.query.all()
    empleados = Empleado.query.all()
    
    trabajos = Trabajo.query.all()
    return render_template('/servicios/servicio.html', vehiculo=vehiculo, piezas=piezas,
                                                    empleados=empleados,empleado=empleado, trabajos=trabajos,
                                                    servicio=servicio,serviciopiezas=serviciopiezas,
                                                    asignacion=asignacion,trabajoprecio=trabajoprecio)

@servicio.route('/create/<int:vehiculo_id>', methods=['GET', 'POST'])
@login_required
def servicio_create(vehiculo_id):
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            flash('Selecione el nombre del servicio')
            return redirect(url_for('vehiculo.get_vehiculo', vehiculo_id=vehiculo_id))

        nuevo_servicio = Servicio(serviciolista_id=name,
                                  vehiculo_id=vehiculo_id)
        db.session.add(nuevo_servicio)
        db.session.commit()
        flash('Servicio creado exictosamente!.')
    return redirect(url_for('vehiculo.get_vehiculo', vehiculo_id=vehiculo_id))

@servicio.route('/<int:vehiculo_id>/<int:servicio_id>', methods=['GET', 'POST'])
@login_required
def servicio_precio(servicio_id, vehiculo_id):
    if request.method == 'POST':
        precio = request.form['precio']
        save = Servicioprecio(precio=precio, servicio_id=servicio_id)
        db.session.add(save)
        db.session.commit()
        flash('Precio Agregado exictoso!.')
    return redirect(url_for('vehiculo.get_vehiculo', vehiculo_id=vehiculo_id))


# registracion de piezas de pintura en general
@servicio.route('/<int:servicio_id>/vehiculo/<int:vehiculo_id>/servicio-pieza', methods=['GET','POST'])
@login_required
def servicio_pieza_create(servicio_id, vehiculo_id):
    if request.method == 'POST':
        multiselect = request.form.getlist('mymultiselect')
        if not multiselect:
            flash('Selecione las pieza')   
        else:
            for pieza in multiselect:
                save = Serviciopieza(servicio_id=servicio_id,pieza_id=pieza) 
                db.session.add(save)
                db.session.commit()
            flash('Piezas registrada')
        
    return redirect(url_for('pintura-general.index', servicio_id=servicio_id, vehiculo_id=vehiculo_id))



@servicio.route('/lista')
@login_required
def servicio_lista():
    form = ServicioListaForm(request.form)
    serviciolista = Serviciolista.query.all() 
    return render_template('/servicios/lista.html', serviciolista=serviciolista,form=form)

@servicio.route('/lista/create', methods=['POST'])
@login_required
def servicio_lista_create():
    form = ServicioListaForm(request.form)
    if request.method == 'POST' and form.validate:
        name = form.name.data
        query = Serviciolista.query.filter_by(name=name).first()
        if query:
            flash('El servicio ya exicte!')
        else:
            save = Serviciolista(name=name)
            db.session.add(save)
            db.session.commit()        
            return redirect(url_for('.servicio_lista'))
    