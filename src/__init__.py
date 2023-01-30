from flask import Blueprint, Flask, make_response, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from os.path import join, dirname, realpath

csrf = CSRFProtect()

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

toolbar = DebugToolbarExtension()

#Carga las Configuraciones
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
WTF_CSRF_SECRET_KEY = 'a random string'
migrate = Migrate(app, db)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static/uploads/..')
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

def allowed_file(file):
    file = file.split('.')
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    return False

#Importa las rutas
from src.views.auth import auth
from src.views.cliente import cliente
from src.views.home import home
from src.views.coche import coche
from src.views.vehiculo import vehiculo
from src.views.servicios import servicio
from src.views.pieza import pieza
from src.views.empleado import empleado
from src.views.trabajo import trabajo
from src.views.asignacion import asignacion
from src.views.pinutra_general import pinturaGeneral
from src.views.pitura_detalle import pinturadetalle
from src.views.producto import producto
from src.views.brillado_completo import brilado_completo
from src.views.historial_ventas import historial_ventas

#Registrando Rutas
app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(cliente)
app.register_blueprint(coche)
app.register_blueprint(vehiculo)
app.register_blueprint(servicio)
app.register_blueprint(pieza)
app.register_blueprint(empleado)
app.register_blueprint(trabajo)
app.register_blueprint(asignacion)
app.register_blueprint(pinturaGeneral)
app.register_blueprint(pinturadetalle) 
app.register_blueprint(producto)
app.register_blueprint(brilado_completo)
app.register_blueprint(historial_ventas)

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

@app.route('/cokies')
def cokies():
    respose = make_response(render_template('cokies.html'))
    respose.set_cookie('custon_cokie', 'Yohan')
    return respose



db.create_all()
