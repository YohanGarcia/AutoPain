from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for
)


from src.models.User import User
from src.models.Cliente import Cliente

from src.views.auth import load_user


from flask_login import current_user, login_required

from src import db

home = Blueprint('index', __name__)

@home.route('/', methods=['GET'])
@login_required
def index():

    clientes = Cliente.query.filter_by(user_id=current_user.id).all()
    
    return render_template('home/index.html', clientes=clientes)