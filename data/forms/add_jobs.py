from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Название волонтерства', validators=[DataRequired()])
    team_leader = IntegerField('Создатель', validators=[DataRequired()])
    des = StringField('Описание', validators=[DataRequired()])
    spher = SelectField('Сфера', choices=['социальное', 'медицинское', 'экологическое', 'культурное'], validators=[DataRequired()])
    age = SelectField('Возраст', choices=['14', '16', '18'], validators=[DataRequired()])
    adress = StringField('Адрес проведения', validators=[DataRequired()])
    contact = StringField('Контакт', validators=[DataRequired()])
    photo = FileField('Фото', validators=[DataRequired()])
    submit = SubmitField('Добавить')