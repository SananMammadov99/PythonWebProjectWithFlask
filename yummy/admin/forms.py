from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField,FloatField
from wtforms.validators import DataRequired


class MenuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Menu')

class FoodForm(FlaskForm):
    name = StringField('Food name', validators=[DataRequired()])
    price = FloatField('Price')
    ingredients = TextAreaField('Ingredients')
    image_url = FileField('Image')
    submit = SubmitField('Add Menu Item')