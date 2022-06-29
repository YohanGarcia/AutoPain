from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired

from src.models.Piesa import Piesa, Precio

class PiesaForm(FlaskForm):
    name = StringField(
        'Piesa',
        id='piesa_create',
        validators=[DataRequired()]
    )

class PrecioForm(FlaskForm):
    precio = IntegerField(
        'Precio',
        id='modelo_create',
        validators=[DataRequired()]
    )
    piesa = SelectField()

    def __init__(self):
        super(PrecioForm, self).__init__()
        self.piesa.choices = [(m.id, m.name) for m in Piesa.query.all()]