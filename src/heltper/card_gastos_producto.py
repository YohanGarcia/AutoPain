from src.heltper.fechas import fecha_hoy, fecha_mañana, fecha_mes, fecha_semana

from src.models.Productos import InventarioProducto


def card_gasto_producto():
# Fecha inicio y fin de hoy
    day_star = fecha_hoy()
    day_end = fecha_mañana()
    semana_star = fecha_semana()
    mes_star = fecha_mes()
    # star fechas del hoy
    today_historial_productos = InventarioProducto.query.filter(
        InventarioProducto.created >= day_star
    ).filter(
        InventarioProducto.created <= day_end
    ).all()
    print(len(today_historial_productos), 'dia')
    today_compras = 0
    for inventario_hoy in today_historial_productos:
        today_compras += inventario_hoy.cantidad * (
            inventario_hoy.cantidad_unidades.unidad * inventario_hoy.productos.precio
        )
    # end fehcas del hoy

    # star fechas de la semana
    semana_historial_productos = InventarioProducto.query.filter(
        InventarioProducto.created >= semana_star
    ).filter(
        InventarioProducto.created <= day_end
    ).all()
    print(len(semana_historial_productos), 'semana')
    semana_compras = 0
    for inventario_semana in semana_historial_productos:
        semana_compras += inventario_semana.cantidad * (
            inventario_semana.cantidad_unidades.unidad * inventario_semana.productos.precio
        )
    # end fechas de la semana

    # star fecha del mes
    mes_historial_productos = InventarioProducto.query.filter(
        InventarioProducto.created >= mes_star
    ).filter(
        InventarioProducto.created <= day_end
    ).all()
    print(len(mes_historial_productos), 'mes')
    month_compras = 0
    for inventario_mes in mes_historial_productos:
        month_compras += inventario_mes.cantidad * (
            inventario_mes.cantidad_unidades.unidad * inventario_mes.productos.precio
        )
    # end fecha del mes
    # today_compras = formated_monto(today_compras)
    # semana_compras = formated_monto(semana_compras)
    # month_compras = formated_monto(month_compras)
    return today_compras,semana_compras,month_compras