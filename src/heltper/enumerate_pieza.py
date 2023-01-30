from src.models.Servicio import Serviciopieza

def enumerate_serviciopiezas(servicio_id):
    serviciopiezas = Serviciopieza.query.filter_by(servicio_id=servicio_id).all()
    return zip(range(len(serviciopiezas)), serviciopiezas)