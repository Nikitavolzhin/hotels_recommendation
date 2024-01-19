from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class HotelRequestForm(FlaskForm):
    want_to_have = StringField("I want to have:", validators=[DataRequired()])
    want_to_avoid = StringField("I want to avoid:")
    rating = DecimalField("Minimal desired rating:", validators=[NumberRange(min=1, max=10), Optional()])
    submit = SubmitField("Submit")
