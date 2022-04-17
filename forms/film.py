from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired


class FilmForm(FlaskForm):
    title = StringField('Название фильма', validators=[DataRequired()])
    rating = FloatField('Рейтинг ( * / 10 )', validators=[DataRequired()])
    year = IntegerField('Год выпуска', validators=[DataRequired()])
    poster = FileField('Постер', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    frame_1 = FileField('Кадр из фильма №1', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    frame_2 = FileField('Кадр из фильма №2', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    frame_3 = FileField('Кадр из фильма №3', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    trailer = FileField('Трейлер (видео)', validators=[FileRequired(), FileAllowed(['mp4', 'webm'])])
    country = StringField('Страна')
    genre = StringField('Жанр', validators=[DataRequired()])
    slogan = StringField('Слоган')
    director = StringField('Режиссёр')
    scenario = StringField('Сценарий')
    producer = StringField('Продюсер')
    operator = StringField('Оператор')
    composer = StringField('Композитор')
    designer = StringField('Художник')
    montage = StringField('Монтаж')
    budget = IntegerField('Бюджет', validators=[DataRequired()])
    fees_in_the_world = IntegerField('Сборы в мире', validators=[DataRequired()])
    audience = StringField('Зрители', validators=[DataRequired()])
    fees_in_russia = IntegerField('Сборы в России')
    world_premiere = StringField('Премьера в мире', validators=[DataRequired()])
    age = IntegerField('Возрастное ограничение', validators=[DataRequired()])
    time = StringField('Длительность фильма (в минутах и часы + минуты)', validators=[DataRequired()])
    short_description = StringField('Краткое описание', validators=[DataRequired()])
    long_description = StringField('Развёрнутое описание', validators=[DataRequired()])


    submit = SubmitField('Submit')
