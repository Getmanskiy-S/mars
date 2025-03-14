from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')
