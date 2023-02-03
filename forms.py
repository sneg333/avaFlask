from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    # validators для проверки вводимых данных
    email = StringField("Email: ", validators=[Email("Некоректный email")])
    # DataRequired() требует что бы в поле пароля был хотя бы один символ
    # Length требует что бы в поле ввода было от 4 до 100 символов  
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="пароль должен быть от 4 до 100 символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    name = StringField