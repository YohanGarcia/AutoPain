from flask import flash, redirect
from src import db


from src.models.Asignacion import Asignacion


def Cambiar_status(id, ruta):
    asignacones = Asignacion.query.filter_by(id=id).first()
    try:
        if asignacones:
            
            asignacones.status = False
            db.session.commit()
            flash('Se canbio el satado')
       
        else:
            flash('Error al cuambiar el stado')
          
    except Exception as e:
        print(e)
     