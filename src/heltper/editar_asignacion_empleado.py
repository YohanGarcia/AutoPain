from flask import flash, redirect
from src import db


from src.models.Asignacion import Asignacion


def Editar_asignacion_empleado(id, precio, empleado, ruta):
    asignacones = Asignacion.query.filter_by(id=id).first()
    print(f'precio: {precio}')
    print(f'empleado: {empleado}')

    try:
        if asignacones:
            if empleado != '' and len(precio) > 0:
                asignacones.empleado_id = empleado
                asignacones.trabajoprecio_id = precio
                db.session.commit()
                flash('Se a actualizado correctamente')
                return redirect(ruta)
            elif empleado:
                asignacones.empleado_id = empleado
                db.session.commit()
                flash('Actualizacion de empleado correctamente')
                return redirect(ruta)
            elif precio:
                asignacones.trabajoprecio_id = precio
                db.session.commit()
                flash('Actualuizacin de precio correctamente')
                return redirect(ruta)
            else:
                flash('Selecione el dato que desea actualizar')
                return redirect(ruta)
        else:
            flash('Error al actualizar')
            return redirect(ruta)
    except Exception as e:
        print(e)
