from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    text = TextAreaField('Введите текст')
    mark = RadioField('', choices=[''] * 10, validators=[DataRequired()])
    submit = SubmitField('Отправить')