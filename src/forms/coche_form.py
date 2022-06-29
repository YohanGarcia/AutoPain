from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField
from wtforms.validators import DataRequired

from src.models.Coche import Marca

class MarcaForm(FlaskForm):
    name = StringField(
        'Marca',
        id='marca_create',
        validators=[DataRequired()]
    )

class ModeloForm(FlaskForm):
    name = StringField(
        'Modelo',
        id='modelo_create',
        validators=[DataRequired()]
    )
    marca = SelectField()

    def __init__(self):
        super(ModeloForm, self).__init__()
        self.marca.choices = [(m.id, m.name) for m in Marca.query.all()]
