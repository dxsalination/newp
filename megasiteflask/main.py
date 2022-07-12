from email.policy import default
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3 as sql


app = Flask(__name__) #создаем обьект на основе класса Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.sqlite' #база данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#база данных
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True) #уникальное поле в табличке в базе данных
    title = db.Column(db.String(300), nullable = False) #поле в табличке в базе данных, нельзя установить пустое значение
    intro = db.Column(db.String(100), nullable = False) #поле в табличке в базе данных, нельзя установить пустое значение
    text = db.Column(db.Text, nullable = False) #поле в табличке в базе данных, нельзя установить пустое значение
    date = db.Column(db.DateTime, default = datetime.utcnow) #поле в табличке в базе данных, будет устанавливаться время добавления статьи

    def __repr__(self):
        return '<Articles %r>' % self.id
        #когда мы будем выбирать какой либо обьект на основе класса АРТИКЛС то нам будет выдаваться сам этот обьект и плюс его айди


#про нас
@app.route('/about') #отслеживаем URL
def index():
    return render_template('about.html') #вывод html страницы


#основная страница
@app.route('/') #отслеживаем URL
def about():
    return render_template('index.html') #вывод html страницы


#все статьи
@app.route('/posts') #отслеживаем URL(все статьи)
def posts():
    articles = Articles.query.order_by(Articles.date.desc()).all() #создаем обьект через который получаем все записи из базы данных
    return render_template('posts.html', articles = articles) #вывод html страницы и передаем обьект в шаблон


#2 страница статей
@app.route('/posts2') #отслеживаем URL
def posts2():
    articles = Articles.query.order_by(Articles.date.desc()).all() #выводим все статьи + сортировка по дате
    return render_template('posts.html', articles = articles) #вывод html страницы

  
#удаление статьи
@app.route('/posts/<int:id>/del') #отслеживаем URL + динамический параметр
def posts_delete(id):
    article = Articles.query.get_or_404(id) #находим определенную статью или ошибка 404

    try:
        db.session.delete(article)
        db.session.commit() #обновление базы данных
        return redirect('/posts')

    except:
        return "При удаление статьи произошла ошибка"

    return render_template('posts-detail.html', article = article) #вывод html страницы


#редактирование статей
@app.route('/posts/<int:id>/update', methods = ['POST', 'GET']) #отслеживаем URL + динамический параметр
def post_update(id):
    article = Articles.query.get(id) #находим определенную статью и передаем в шаблон
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit() #обновление базы данных
            return redirect('/posts')

        except:
            return "При редактировании статьи произошла ошибка"
    else:
        
        return render_template("post_update.html", article=article) #вывод html страницы + передача статьи


#переход на полную статью
@app.route('/posts/<int:id>') #отслеживаем URL + динамический параметр
def posts_detail(id):
    article = Articles.query.get(id) #находим определенную статью
    return render_template('posts-detail.html', article = article) #вывод html страницы


#создание статьи
@app.route('/create-article', methods = ['POST', 'GET']) #отслеживаем URL + методы передачи данных(прямой заход на страницу и из формы)
def create_article():
    if request.method == 'POST':
        title = request.form['title'] #получаем данные из формы
        intro = request.form['intro'] #получаем данные из формы
        text = request.form['text'] #получаем данные из формы

        article = Articles(title = title, intro = intro, text = text) #обьект на основе класса АРТИКЛС + передаем обьекты формы

        try:
            db.session.add(article) #добавляем обьект  
            db.session.commit() #сохраняем обьект  
            return redirect('/posts')
            return redirect('/posts2')
        except:
            return "При добавление статьи произошла ошибка"
    else:
        return render_template("main.html") #вывод html страницы


if __name__ == "__main__":
    app.run(debug = True) #Запуск локального сервера