from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, validators, Form, IntegerField


class ClienteForm(Form):
   username = StringField('Nombre',
                           [
                               validators.length(
                                   min=3, max=25, message='Ingrese un nombre valido!.'),
                               validators.DataRequired(
                                   message='El Nombre es requerido')
                           ]
                           )
   lestname = StringField('Apellido',
                           [
                               validators.Regexp(r'^\+1 \d{3}-\d{3}-\d{4}$', message='Phone number must be in the format +1 XXX-XXX-XXXX')
                           ])

   telefono = StringField('Telefono',
                           [
                               validators.length(
                                   min=3, max=25, message='Ingrese un Telefono valido!.'),
                               validators.DataRequired(
                                   message='El Telefono es requerido')
                           ])
   cedula = StringField('Cedula')
   direccion = StringField('Direccion')