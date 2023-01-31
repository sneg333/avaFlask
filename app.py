import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, g, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash #генерация данных пароля
from FDataBase import FDataBase
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin

DATABASE = 'tmp/app.db'
DEBUG = True
SECRET_KEY = '112244'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'app.db')))

login_manager = LoginManager(app)
#перенаправляем неавторизованного пользователя
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для досутпа к закрытым страницам"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

#   функция для установления соединения с БД
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

### делаем глобальную функцию, что бы она была доступной во всех запросах
dbase = None
### def before_request(): = соединение с БД перед выполеннием запроса
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)



###     ОТОБРАЖЕНИЕ ДОМАШНЕЙ СТРАНИЦЫ
@app.route('/')
def home():
    print(url_for('home'))
    return render_template('home.html', title="домашняя", menu=dbase.getMenu(), news=dbase.getNewsAnonce(), products=dbase.getProductsAll())

####    ОТОБРАЖЕНИЕ СТРАНИЦЫ КОНТАКТЫ
@app.route('/contact')
def contact():
    return render_template('contact.html', title="Контакты", menu=dbase.getMenu(), contact=dbase.getContact())

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

###     ОТОБРАЖЕНИЕ СТРАНИЦЫ ЛОГИН
@app.route('/login', methods=["POST", "GET"])
def login():
    # если пользователь авторизован, перенаправляем его на другую стр если 
    # он пытается второй раз авторизоватсья
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            #реализайция кнопки запомнить меня
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            # перенаправляем на стр которую смотрел неавторизованный пользователь
            # он попадает на неё после регистрации
            return redirect(request.args.get("next") or url_for('profile'))

        flash("неварная пара логин/пароль", "error")
    return render_template('login.html', title="авторизация", menu=dbase.getMenu())

###     ОТОБРАЖЕНИЕ СТР РЕГИСТРАЦИИ
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 2 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("вы успешно зарегистрированы", "soccess")
                return redirect(url_for('login'))
            else:
                flash("ошибка при добавлении в БД", "error")
        else:
            flash("неверно заполнены поля", "error")

    return render_template('register.html', title="регистрация", menu=dbase.getMenu())

### ВЫЙТИ ИЗ ПРОФИЛЯ
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("вы вышли из аккаунта", "soccess")
    return redirect(url_for('login'))

###страница профиля
@app.route('/profile')
#доступна только для авторизованных пользователей
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Выйти из профиля</a>
                <p>user info: {current_user.get_id()}"""

###     ОТОБРАЖЕНИЕ ВСЕХ НОВОСТЕЙ
@app.route('/news')
def news():
    return render_template('news.html', title="Новости", menu=dbase.getMenu(), news=dbase.getNewsAnonce())

#####   ДОБАВЛЕНИЕ НОВОЙ НОВОСТИ
@app.route('/createpost', methods=["POST", "GET"])
def createpost():
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

###     ОТОБРАЖЕНИЯ ОДНОЙ НОВОСТИ
@app.route("/new/<int:id_new>")
def postDetail(id_new):
    title, full_text = dbase.getNew(id_new)
    if not title:
        abort(404)
    return render_template('new-detail.html', menu=dbase.getMenu(), title=title, full_text=full_text)

###     ОТОБРАЖЕНИЯ ОДНОГО ПРОДУКТА
@app.route("/product/<alias>")
@login_required
def productDetail(alias):
    title_product, body_product = dbase.getProduct(alias)
    if not title_product:
        abort(404)
    return render_template('product-detail.html', menu=dbase.getMenu(), title_product=title_product, body_product=body_product)

####################################### СТРАНИЦА АДМИНИСТРИРОВАНИЯ
@app.route('/admin')
def admin():
    return render_template('admin.html', title="администрирование", menu=dbase.getMenu(), adminpanel=dbase.getAdminPanel())

#############ДОБАВИТЬ ПРОДУКТ
@app.route('/addproduct', methods=["POST", "GET"])
def addproduct():

    if request.method == 'POST':
        if len(request.form['title_product']) > 4 and len(request.form['body_product']) > 10:
            res7 = dbase.addproduct(request.form['title_product'], request.form['body_product'], request.form['url'])
            if not res7:
                flash('ошибка отправки', category='error')
            else:
                flash('сообщение отправлено успешно!!!', category='success')
        else:
            flash('ошибка отправки', category='error')

    return render_template('addproduct.html', title="добавить продукт", menu=dbase.getMenu(), )

######################  404  #####################
@app.errorhandler(404)
def pageNotFount(error):
    return render_template('404.html', title="страница не найдена", menu=dbase.getMenu())

if __name__ == "__main__":
    app.run(debug=True)

