1 flash - сообщения после выполнения действий, например кведомление о том, 
    что покупка состоялась, или произошла ошибка
2 request - обработка формы с методом GET или POST
3 url_for - подключение статики
4 render_template рендерить html файл 
5 from flask_sqlalchemy import SQLAlchemy - библиотека для работы с базой данных

6 создание базы данных:
    python3 
        from app import create_db
          create_db() 
          exit() 


7 для кодирования пароля при регистрации
сначала импортируем две фурнкции: generate_password_hash и check_password_hash
    python3 
        from werkzeug.security import generate_password_hash, check_password_hash

8 flask-Login
    pip install flask-login

    в app.py
    from flask_login import LoginManager

    login_manager = LoginManager(app)
