from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired


class DFAInputForm(FlaskForm):
    states = IntegerField("States", validators=[InputRequired()])
    symbols = IntegerField("Symbols", validators=[InputRequired()])
    submit = SubmitField("Submit")
