from flask import flash, redirect
from src import db

from src.models.Servicio import Serviciopieza
from src.models.Asignacion import Asignacion


def Eliminar_servicio_pieza(id, ruta):
    servicio_pieza = Serviciopieza.query.filter_by(id=id).first()
    asignacion = Asignacion.query.filter_by(serviciopieza_id=servicio_pieza.id).first()
    try:
        if servicio_pieza:
            db.session.delete(servicio_pieza)
            if asignacion:
                db.session.delete(asignacion)
            db.session.commit()
            
            flash('Se a eliminado correctamente')
            return redirect(ruta)
        else:
            flash('Error al Eliminar')
            return redirect(ruta)
    except Exception as e:
        print(e)
