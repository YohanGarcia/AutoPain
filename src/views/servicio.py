from math import pi
from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from flask_login import current_user, login_required

from src import db

from src.models.servicios import Pinturageneral, Servicio, Pinturageneralpiesa
from src.models.Vehiculo import Vehiculo
from src.models.Piesa import Piesa

servicio = Blueprint('servicio', __name__, url_prefix='/servicio')

@servicio.route('/<int:servicio_id>/vehiculo/<int:vehiculo_id>/pintura-general', methods=['GET', 'POST'])
@login_required
def main(servicio_id,vehiculo_id):
    vehiculos = Vehiculo.query.filter_by(id=vehiculo_id).first()
    servicios = Servicio.query.filter_by(id=servicio_id).first()
    pinturageneral = Pinturageneral.query.filter_by(servicio_id=servicio_id).first()
    #pinturageneralpiesas = Pinturageneralpiesa.query.filter_by(pinturageneral_id=pinturageneral.id).all()

    piesas = Piesa.query.all()
    
    if request.method == 'POST':
        precio = request.form.get('precio')
        nuevo = Pinturageneral(precio=int(precio), servicio_id=servicio_id)
        db.session.add(nuevo)
        db.session.commit()
        print('entro squi')
        return redirect(url_for('servicio.main', vehiculo_id=vehiculos.id, servicio_id=servicios.id))
    
    """  else:
        if pinturageneralpiesas:
            print('hay datos')
            pass
        else:
            print('No hay datos')
            for piesa in piesas:
                piesa_id = piesa.id
                nueva_piesa = Pinturageneralpiesa(piesa_id=piesa_id, pinturageneral_id=pinturageneral.id)
                db.session.add(nueva_piesa)
                db.session.commit() """
    
    return render_template(
        'servicios/pintura-general.html', 
        servicios=servicios, 
        vehiculo=vehiculos,
        pinturagenerals=pinturageneral,
       # pinturageneralpiesas=pinturageneralpiesas,
        piesas=piesas
    )