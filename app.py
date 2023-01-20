import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, g
from FDataBase import FDataBase

DATABASE = 'tmp/app.db'
DEBUG = True
SECRET_KEY = '112244'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'app.db')))

#функция для установления соединения с БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

from datetime import datetime
# menu =[
#         {"name": "Домашняя", "url": "/"},
#         {"name": "Контакты", "url": "contact"},
#         {"name": "Добавить поcт", "url": "createpost"},
#         {"name": "новости", "url": "news"},
#         {"name": "вход", "url": "login"},
#     ]
@app.route('/')
def home():
    print(url_for('home'))
    db = get_db()
    dbase = FDataBase(db)
    return render_template('home.html', title="домашняя", menu=dbase.getMenu())

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/contact')
def contact():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('contact.html', title="Контакты", menu=dbase.getMenu())

@app.route('/login')
def login():
    print(url_for('login'))
    return render_template('login.html', title="авторизация", menu=menu)

@app.route('/news')
def news():
    print(url_for('news'))
    return render_template('news.html', title="Новости", menu=menu)

@app.route('/createpost', methods=["POST", "GET"])
def createpost():
    if request.method == 'POST':
            if len(request.form['title']) > 2:
                flash('сообщение отправлено успешно!!!', category='success')
            else:
                flash('ошибка отправки', category='error')

    print(request.form)
    print(url_for('createpost'))
    return render_template('createpost.html', title="добавить пост", menu=menu)

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('404.html', title="страница не найдена", menu=menu)

if __name__ == "__main__":
    app.run(debug=True)