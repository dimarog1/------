from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    text = TextAreaField('Введите текст')
    mark_1 = RadioField('')
    mark_2 = RadioField('')
    mark_3 = RadioField('')
    mark_4 = RadioField('')
    mark_5 = RadioField('')
    submit = SubmitField('Отправить')
