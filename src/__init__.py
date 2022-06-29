from flask import Blueprint, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
#Carga las Configuraciones
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
WTF_CSRF_SECRET_KEY = 'a random string'

app.config['CORS_HEADERS'] = 'Content-Type'

#Importa las rutas
from src.views.auth import auth
from src.views.cliente import cliente
from src.views.home import home
from src.views.coche import coche
from src.views.vehiculo import vehiculo
from src.views.piesa import piesa
from src.views.servicio_lista import lista
from src.views.servicio import servicio
#Registrando Rutas

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(cliente)
app.register_blueprint(coche)
app.register_blueprint(vehiculo)
app.register_blueprint(piesa)
app.register_blueprint(lista)
app.register_blueprint(servicio)

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500


#background process happening without any refreshing
@app.route('/background_process_test/<string:id>')
def background_process_test(id):
    print ("Hello")
    print(int(id))
    return ("nothing")
    
db.create_all()