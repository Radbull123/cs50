import datetime
import re
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_session import Session
from sqlalchemy import or_
from create_db import *


app = Flask(__name__, static_folder=f"{os.getcwd()}\\static")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_USE_SIGNER"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(hours=5)

# Initialize app
app.wsgi_app = ProxyFix(app.wsgi_app)
Session(app)

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/home/<user>')
def logged_user(user):
    return render_template("home.html")


@app.route('/registration', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form['password']
        repeat_password = request.form['rep_password']
        if password != repeat_password:
            flash("Repeated Password should be matched with Password.", category='danger')
        elif re.search(r'[a-zA-Z]+', username) is None:
            flash("Please, enter at least one letter in your username.", category='danger')
        # regex which searches weak password
        elif re.search(r'^(\w*|\W*)$|^.{0,5}$', password):
            flash(
                f"The password is to weak, please set the password which contains min 6 "
                "characters: letter, symbol and numeric", category='warning')
        elif db.query(User).filter(User.username == username).first():
            flash(f"This username has been already registered, please choose another username", category='warning')
        elif db.query(User).filter(User.username == username).first() is None:
            current_user = User(username=username, password=password)
            db.add(current_user)
            db.commit()
            session["username"] = request.form["username"]
            flash(f"Congratulation {session['username']} you have been registered", category='success')
            return redirect(url_for('index'))

    return render_template("users/registration.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.query(User).filter(User.username == username).first()
        if user is not None and\
                re.search(rf'^{password}$', user.password) is not None:
            flash(f"Welcome back {username}!!!", category='success')
            session['username'] = request.form["username"]
            return redirect(url_for('logged_user', user=username))
        else:
            flash("Username or password have been entered incorrect, please try again", category='danger')

    return render_template("users/login.html")


@app.route("/logout", methods=('POST', 'GET'))
def logout():
    if request.method == "POST":
        yes_btn = request.form.get('yes')
        no_btn = request.form.get('no')
        if yes_btn is not None:
            flash(f"Good bye {session.get('username')}!!!", 'info')
            session.pop('username', None)
            session.modified = True
            return redirect(url_for('index'))
        elif no_btn is not None:
            flash(f"We are pleased {session['username']}, you are staying with us", 'info')
            return redirect(url_for('logged_user', user=session['username']))

    return render_template('users/logout.html')


@app.route("/all_books")
def books_list(books=None):
    if books is None or db.query(Books).first() is not None:
        books = db.query(Books).all()
    return render_template("books/books_page.html", books=books)


@app.route("/search_page", methods=("POST", "GET"))
def searching_page(searching_value=None, matched_books=None):
    if request.method == "POST":
        searching_value = request.form.get("searching_value")
        matched_books = db.query(Books).filter(
            or_(Books.isbn.like(f"%{searching_value}%"), Books.title.like(f"%{searching_value}%"),
                Books.author.like(f"%{searching_value}%"), Books.year.like(f"%{searching_value}%"))).all()
        if not matched_books:
            matched_books = None
            flash(f"There is no book with requested value '{searching_value}'", "warning")

    return render_template("books/search_page.html", searching_value=searching_value, matched_books=matched_books)


if __name__ == "__main__":
    app.run(debug=True)
