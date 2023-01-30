from wtforms import StringField, validators, Form

class ServicioListaForm(Form):
    name = StringField('name',
                         [
                            validators.length(min=3, max=25, message='Ingrese un nombre valido!.'),
                            validators.DataRequired(message='El Nombre es requerido')
                         ]
                         )