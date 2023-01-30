import functools
from venv import create
from flask import(
    render_template, redirect, url_for,
    Blueprint, flash, g, request, session
)
from flask_login import login_user, logout_user

from src.forms.register import RegisterForm

from src.forms.register import RegisterForm
from src.forms.login import LoginForm

from src.models.User import User
from src import db, login_manager

auth = Blueprint('auth', __name__, url_prefix='/auth')


#Registrar usuarios
@auth.route('/register', methods=['GET', 'POST'])
def create_register():
    register_form = RegisterForm(request.form)
    if request.method == 'POST' and register_form.validate():
        user = User(register_form.username.data,
                    register_form.password.data,
                    register_form.email.data
                    )
        db.session.add(user)
        db.session.commit()
        flash('registro exictoso')
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('/auth/register.html', form=register_form)

#Iniciar Sesion
@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_forms = LoginForm(request.form)
    if request.method == 'POST' and login_forms.validate():
        username = login_forms.username.data
        password = login_forms.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            flash(f'Bienvinido {login_forms.username.data}')
            login_user(user)
            return redirect(url_for('index.index'))
        else:
            error_message = 'Usuario o contraseña invalida!.'
            flash(error_message)
            return redirect(url_for('auth.login'))
    return render_template('/auth/login.html', form=login_forms, msg='Email already registered',
                           success=False,)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))