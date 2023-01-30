from flask import (
    render_template,
    Blueprint, flash, g, redirect,
    request, url_for, session
)
from flask_login import current_user, login_required
from src.helper import current_date_format
from src.heltper.card_gastos_producto import card_gasto_producto
from src.heltper.fechas import fecha_hoy, fecha_mañana, fecha_mes, fecha_semana
from src.heltper.formato import format_number

from src.models.User import User
from src.models.Cliente import Cliente
from src.models.Empleados import Empleado
from src.models.Productos import Producto, InventarioProducto

from src import db
home = Blueprint('index', __name__)


@home.route('/', methods=['GET'])
@login_required
def index():
    card = card_gasto_producto()
    print(card)
    empleados = Empleado.query.all()
    clientes = Cliente.query.all()
    print(current_user.username, 'usuario')
    
    return render_template(
        'home/index.html',
        formated_number=format_number,
        current_date_format=current_date_format,
        clientes=clientes,
        empleados=empleados,
        today_compras=card[0],
        semana_compras=card[1],
        month_compras=card[2],
        
    )
