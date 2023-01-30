from collections import defaultdict


def Empleado_total(asignaciones):
    empleados_total = defaultdict(int)

    for asignacion in asignaciones:
        empleados_total[asignacion.empleados.name,asignacion.empleados.lastname] += asignacion.trabajoprecios.precio
    
    return empleados_total