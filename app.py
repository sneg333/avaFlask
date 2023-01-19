from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ava.db'
db = SQLAlchemy(app)

class New(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    mini_text = db.Column(db.String(300), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<New %r>' % self.id

menu =[
        {"name": "Домашняя", "url": "/"},
        {"name": "Контакты", "url": "contact"},
        {"name": "Добавить поcт", "url": "createpost"},
        {"name": "новости", "url": "news"},
        {"name": "вход", "url": "login"},
    ]

@app.route('/')
def home():
    print(url_for('home'))
    return render_template('home.html', title="домашняя", menu=menu)

@app.route('/contact')
def contact():
    print(url_for('contact'))
    return render_template('contact.html', title="Контакты", menu=menu)

@app.route('/login')
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

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