from flask import(
    render_template, Blueprint, flash, 
    redirect, request, url_for
)
from collections import Counter

from flask_login import login_required
from src import db
from src.helper import current_date_format
from src.heltper.formato import format_number
from src.models.Productos import HistorialVentas



historial_ventas = Blueprint('historial-ventas', __name__, url_prefix='/producto/historial-ventas')

@historial_ventas.route('/')
@login_required
def index():
    historial_ventas_products = HistorialVentas.query.all()

    ganacia_total = 0
    gastos_total = 0
    venta_total = 0
    for historial_ventas in historial_ventas_products:
        ganacia_total += historial_ventas.cantidad * (historial_ventas.precio - historial_ventas.productos.precio)
        gastos_total += historial_ventas.productos.precio * historial_ventas.cantidad
        venta_total += historial_ventas.cantidad * historial_ventas.precio

    print(f'Ganancia Total {ganacia_total}')
    print(f'Gastos Total {gastos_total}')
    print(f'Venta total {venta_total}')
    return render_template('productos/historial-ventas.html', 
        historial_ventas_products=historial_ventas_products,
        ganacia_total=ganacia_total,
        gastos_total=gastos_total,
        venta_total=venta_total,
        current_date_format=current_date_format,
        format_number=format_number)