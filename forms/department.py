from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = IntegerField('ID начальника', validators=[DataRequired()])
    members = StringField('Список членов (через запятую)', validators=[DataRequired()])
    email = EmailField('Email департамента', validators=[DataRequired()])
    submit = SubmitField('Submit')