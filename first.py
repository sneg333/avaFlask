from flask import Flask, render_template, url_for, request, flash
app = Flask(__name__)
app.config['SECRET_KEY'] = '112244'

menu =[
        {"name": "Домашняя", "url": "/"},
        {"name": "Контакты", "url": "contact"},
        {"name": "Добавить поcт", "url": "createpost"},
    ]

@app.route('/')
def home():
    print(url_for('home'))
    return render_template('home.html', title="домашняя", menu=menu)

@app.route('/contact')
def contact():
    print(url_for('contact'))
    return render_template('contact.html', title="Контакты", menu=menu)

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