from typing import List
from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Article, User
from flask_migrate import Migrate
from forms import ArticleForm, LoginForm, RegistrationForm
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from hashlib import sha256
import os

SECRET_KEY = "somesecretvalue"
import sqlite3
from models import User, Article, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?check_same_thread=False'
app.config['SECRET_KEY'] = os.environ["SECRET_KEY_MYSITE"] = "aaaaaaaaaaaaaaaaaaa"
db.app = app
db.init_app(app)
Bootstrap(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def hello_world():
    return render_template('site.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=("GET", "POST"))
def reg():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        passwordcode = request.form.get("password")
        password = sha256(passwordcode.encode("utf-8")).hexdigest()
        existing_user = User.query.filter(User.username.like(username) | User.email.like(email)).first()
        if existing_user is not None:
            abort(400)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("about"))
    return render_template('register.html')


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("site"))


@app.route('/create', methods=("GET", "POST"))
@login_required
def register():
    articles = Article.query.filter_by(username=current_user.username).all()
    form = ArticleForm()
    if request.method == 'POST':
        print('sx')
        title = request.form.get("title")
        body = request.form.get("body")
        article = Article(title=title, body=body, username=current_user.username)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("register"))
    return render_template('create.html', form=form, articles=articles)

@app.route('/create/<int:article_id>', methods=("POST",))
@login_required
def edit_article(article_id):
    article: Article = Article.query.filter_by(id=article_id).first()
    article.title = request.form.get("title")
    article.body = request.form.get("body")
    db.session.add(article)
    db.session.commit()
    return redirect(url_for("register", article_id=article.id))

@app.route('/delete/<int:article_id>', methods=("GET",))
@login_required
def delete(article_id):
    article: Article = Article.query.filter_by(id=article_id).first()
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("register", article_id=article.id))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get("username")
        passwordcode = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user is None or user.check_password(passwordcode) == False:
            abort(400)
        login_user(user)
        return redirect(url_for("about"))
    return render_template("login.html", form=form)


@app.route('/verify/')
def verify():
    return render_template('verify.html')


if __name__ == '__main__':
    app.run()
