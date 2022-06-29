from tkinter.tix import Select
from flask_wtf import FlaskForm, Form

from wtforms.fields import StringField, SelectField
from wtforms.validators import DataRequired

from wtforms_sqlalchemy.fields import QuerySelectField

from src.models.Coche import Marca, Modelo

def get_marca():
    return Marca.query.all()

class VehiculoForm(FlaskForm):
    marca = SelectField(
       'Placa',
        id='car_brand',
        validators=[DataRequired("Debe Selecione una Marca")]
    )
    modelo = SelectField(
        'Modelo',
        id='car_models',
        validators=[DataRequired("Debe Selecionar un Modelo")]
    )
    placa = StringField(
        'Placa',
        id='placa_create',
        validators=[DataRequired("Ingrese una Placa")]
    )

    age = StringField(
        'Año',
        id='age_create',
        validators=[DataRequired("Ingre el Año del vehiculo")]
    )

    color = StringField(
        'Color',
        id='color_create',
        validators=[DataRequired("Ingrese el Color")]
    )

    def __init__(self):
        super(VehiculoForm, self).__init__()
        self.marca.choices = [(c.id, c.name) for c in Marca.query.all()]