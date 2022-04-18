from flask_security.forms import RegisterForm, LoginForm
from flask_security.forms import SubmitField, PasswordField, Required, StringField


class ExtendedRegisterForm(RegisterForm):
    email = StringField('Почта', validators=[Required()])
    nickname = StringField('Имя пользователя', validators=[Required()])
    password = PasswordField('Пароль', validators=[Required()])
    password_confirm = PasswordField('Подтвердите пароль', validators=[Required()])
    submit = SubmitField('Зарегистрироваться')


class ExtendedLoginForm(LoginForm):
    email = StringField('Почта', [Required()])
    password = PasswordField('Пароль', [Required()])
    submit = SubmitField('Войти')

    def validate(self):
        response = super(ExtendedLoginForm, self).validate()
        return response


class EditUser(LoginForm):
    email = StringField('Почта')
    nickname = StringField('Имя пользователя')
    password = PasswordField('Пароль')