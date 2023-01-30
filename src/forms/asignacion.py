from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField
from wtforms.validators import DataRequired

from src.models.Empleados import Empleado


class EmpleadoForm(FlaskForm):
    
    name = SelectField()

    def __init__(self):
        super(EmpleadoForm, self).__init__()
        self.name.choices = [(m.id, m.name) for m in Empleado.query.all()]