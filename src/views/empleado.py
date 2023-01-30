from fileinput import filename
from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from flask_login import login_required
from werkzeug.utils import secure_filename
import os

from src import db, allowed_file, app
from src.models.Empleados import Empleado

empleado = Blueprint('empleado', __name__, url_prefix='/empleado')

@empleado.route('create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            lastname = request.form.get('lastname')
            telefono = request.form.get('telefono')
            telefonocasa = request.form.get('telefonocasa')
            correo = request.form.get('correo')
            nacimiento = request.form.get('nacimiento')
            cedula = request.form.get('cedula')
            foto = request.files['foto']
            empleado = Empleado.query.filter_by(cedula=cedula,correo=correo, telefono=telefono).first()
            if empleado:
                flash(f'El empleado {name} {lastname} exicte!.')
                return redirect(url_for('empleado.create'))
            filename = secure_filename(foto.filename)
            nuevo_empleado = Empleado(
                            name=name,
                            lastname=lastname,
                            telefono=telefono,
                            telefonocasa=telefonocasa,
                            cedula=cedula,
                            correo=correo,
                            foto=filename,
                            nacimiento=nacimiento,
                        )
            db.session.add(nuevo_empleado)
            db.session.commit() 
            flash('Empleado registrado con exicto!.')
            if foto and allowed_file(filename):
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('empleado.create'))
        except Exception as e:
            print(e)
            flash('Error creating hay datos que pertesen a otro usuario')
    return render_template('empleado/created.html')