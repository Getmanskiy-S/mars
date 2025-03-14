from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название', validators=[DataRequired()])
    team_leader = IntegerField('id руководителя', validators=[DataRequired()])
    work_size = StringField('Объем работ', validators=[DataRequired()])
    collaborators = StringField('Исполнители', validators=[DataRequired()])
    is_finished = BooleanField('Работа выполнена?')

    submit = SubmitField('Представление')