from wtforms import Form, StringField, PasswordField, validators, EmailField
from src.models.User import User

class RegisterForm(Form):
    username = StringField('Username',
    [
        validators.DataRequired(message='El username es requerido!.'),
        validators.length(min=3, max=25, message='Ingrese un username valido!.')
    ]
    )
    email = EmailField('Email',
        [
            validators.DataRequired('El email es requerido!.'),
            validators.Email(message='Ingrese un correo valido!.'),
            validators.length(min=4, max=35, message='Ingrese un correo valido!.')
        ]
    )
    password = PasswordField('Password',
        [
            validators.DataRequired(message='El password es requerido!.')
        ]
    )

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya esta registrado')