1 flash - сообщения после выполнения действий, например кведомление о том, 
    что покупка состоялась, или произошла ошибка
2 request - обработка формы с методом GET или POST
3 url_for - подключение статики
4 render_template рендерить html файл 
5 from flask_sqlalchemy import SQLAlchemy - библиотека для работы с базой данных

6 создание базы данных:
    python3 
        from app import db
          db.create_all() 
          exit() 