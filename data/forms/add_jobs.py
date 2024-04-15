from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Название волонтерства', validators=[DataRequired()])
    team_leader = IntegerField('Создатель', validators=[DataRequired()])
    des = StringField('Описание', validators=[DataRequired()])
    spher = StringField('Сфера', validators=[DataRequired()])
    age = SelectField('Возраст', choices=['14', '16', '18'], validators=[DataRequired()])
    adress = StringField('Адрес проведения', validators=[DataRequired()])
    submit = SubmitField('Добавить')