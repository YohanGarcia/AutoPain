import functools
from venv import create
from flask import(
    render_template, redirect, url_for,
    Blueprint, flash, g, request, session
)
from flask_login import current_user, login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

from src.forms.user_form import LoginForm, CreateAccountForm

from src.models.User import User
from src import db, login_manager

auth = Blueprint('auth', __name__, url_prefix='/auth')


#Registrar usuarios
@auth.route('/register', methods=['GET','POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        lastname = request.form['lastname']
        email = request.form['email']
        empresa = request.form['empresa']
        password = request.form['password']
        
        error = None
        if not username:
            error = 'Se requiere nombre de usuario'
        elif not lastname:
            error = 'Se requiere el apallido'
        elif not email:
            error = 'Se requiere el correo'
        elif not empresa:
            error = 'Se requiere el nombre de la empresa'
        elif not password:
            error = 'Se requiere una contraseña'
        flash(error)
        user_name = User.query.filter_by(username=username).first()
        if user_name:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)
            
        nuevo_user = User(
                    username=username,
                    lastname=lastname,
                    empresa=empresa,
                    email=email,
                    password=generate_password_hash(password)
        )
        db.session.add(nuevo_user)
        db.session.commit()
        flash('registro exictoso')
        logout_user()
        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)
    else:
        return render_template('accounts/register.html', form=create_account_form)

#Iniciar Sesion
@auth.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index.index'))

        flash('password incorrecta')
        
        return render_template('accounts/login.html', 
                                msn="Usuario o contraseña incorrectos", 
                                form=login_form)
    
    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    return redirect(url_for('cliente.index'))

#Cerrar session
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))