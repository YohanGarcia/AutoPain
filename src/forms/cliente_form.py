from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ClienteForm(FlaskForm):
    username = StringField('Username',
                         id='username_cliente',
                         validators=[DataRequired()])
    
    lastname = StringField('Lastname',
                         id='lastname_cliente',
                         validators=[DataRequired()])

    telefono = StringField('Telefono',
                         id='telefono_cliente',
                         validators=[DataRequired()])
