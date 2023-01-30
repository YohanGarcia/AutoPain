from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    username = StringField('Username',
    [
        validators.DataRequired(message='El usernamae es requerido!.'),
        validators.length(min=3, max=25, message='Ingrese un username valido!.')
    ])
    password = PasswordField('Passwprd',
    [
        validators.DataRequired(message='La contraseña es requerida!.')
    ])