from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired

class CupcakeForm(FlaskForm):
    """Form for adding a new cupcake"""

    flavor = StringField("Flavor",
                         validators=[InputRequired()])
    image = StringField("Image URL")
    size = StringField("Size",
                        validators=[InputRequired()])
    rating = FloatField("Rating",
                        validators=[InputRequired()])