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
    return render_template('contact.html', title="Контакты", menu=dbase.getMenu(), contact=dbase.getContact())

@app.route('/login')
def login():
    print(url_for('login'))
    return render_template('login.html', title="авторизация", menu=menu)

@app.route('/news')
def news():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('news.html', title="Новости", menu=dbase.getMenu(), news=dbase.getNewsAnonce())


@app.route('/createpost', methods=["POST", "GET"])
def createpost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['title']) > 4 and len(request.form['full_text']) > 10:
            res = dbase.createpost(request.form['title'], request.form['full_text'])
            if not res:
                flash('ошибка отправки', category='error')
            else:
                flash('сообщение отправлено успешно!!!', category='success')
        else:
            flash('ошибка отправки', category='error')

    return render_template('createpost.html', title="добавить пост", menu=dbase.getMenu())

@app.route("/new/<int:id_new>")
def postDetail(id_new):
    db = get_db()
    dbase = FDataBase(db)
    title, full_text = dbase.getNew(id_new)
    if not title:
        abort(404)

    return render_template('new-detail.html', menu=dbase.getMenu(), title=title, full_text=full_text)

@app.errorhandler(404)
def pageNotFount(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template('404.html', title="страница не найдена", menu=dbase.getMenu())

if __name__ == "__main__":
    app.run(debug=True)