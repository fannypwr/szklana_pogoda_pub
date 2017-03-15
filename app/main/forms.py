from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

ADDRESS = 'Type city name'
SEARCH = 'Search'


class SearchForm(FlaskForm):
    address = StringField(ADDRESS, validators=[DataRequired()])
    submit = SubmitField(SEARCH)