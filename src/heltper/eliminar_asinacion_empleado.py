from flask import flash, redirect
from src import db


from src.models.Asignacion import Asignacion


def Eliminar_asignacion_empleado(id, ruta):
    asignacones = Asignacion.query.filter_by(id=id).first()
    try:
        if asignacones:
            db.session.delete(asignacones)
            db.session.commit()
            flash('Se a eliminado correctamente')
            return redirect(ruta)
        else:
            flash('Error al Eliminar')
            return redirect(ruta)
    except Exception as e:
        print(e)
