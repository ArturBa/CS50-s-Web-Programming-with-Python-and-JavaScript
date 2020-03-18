import requests
from flask import Flask, session, render_template, jsonify, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from utils import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/user')
def user():
    if session['user']:
        print(session['user'][3])
        return render_template('user.html', user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register_authorization', methods=['POST'])
def register_authorization():
    if request.method != 'POST':
        message = {'type': 'warning', 'value': f'{request.method} is not POST\nWrong method used'}
        flash(message)
        return redirect(url_for('register'))
    post_username = request.form.get('username')
    print(post_username)
    post_password = code_password(str(request.form.get('password')))
    post_name = str(request.form.get('name'))
    try:
        db.execute("INSERT INTO users (username, password, name) VALUES (:username, :password, :name)",
                   {"username": post_username, "password": post_password, "name": post_name})
        db.commit()
        message = {'type': 'success', 'value': 'User created'}
        flash(message)
        return redirect(url_for('login'))
    except Exception as exception:
        print(exception)
        message = {'type': 'warning', 'value': 'User with that username already exist'}
        flash(message)
        return redirect(url_for('register'))


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    session['user'] = None
    return redirect(url_for('index'))


@app.route('/login_authorization', methods=['POST'])
def login_authorization():
    if request.method != 'POST':
        message = {'type': 'warning', 'value': f'{request.method} is not POST\nWrong method used'}
        flash(message)
        return redirect(url_for('login'))
    post_username = str(request.form.get('username'))
    post_password = code_password(str(request.form.get('password')))

    result = db.execute("SELECT * FROM users WHERE username=:username AND password=:password;",
                        {'username': post_username, 'password': post_password}).fetchmany(1)
    if result is None:
        message = {'type': 'warning', 'value': 'Login and password not matching'}
        flash(message)
        return redirect(url_for('login'))
    else:
        session['user'] = result[0]
        return redirect(url_for('index'))


@app.route('/books')
def books():
    """Return detail about all books"""
    _books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=_books)


@app.route('/book/<book_isbn>')
def book(book_isbn):
    """Return detail about a single book"""
    try:
        _book = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": book_isbn}).fetchmany(1)[0]
        _review = db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id = users.id WHERE book_isbn=:isbn;",
                             {"isbn": book_isbn}).fetchall()
        goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
                                 params={"key": os.getenv('GOODREADS_KEY'), "isbns": book_isbn})
        if goodreads.status_code == 200:
            goodreads_data = goodreads.json()['books'][0]
        else:
            goodreads_data = None
        return render_template("book.html", book=_book, reviews=_review, user=session['user'], goodreads=goodreads_data)
    except Exception as exception:
        print(type(exception))
        return render_template("error.html", message="Book not found")


@app.route('/add_opinion', methods=['POST'])
def add_opinion():
    if request.method != 'POST':
        return redirect(url_for('index'))
    try:
        db.execute("INSERT INTO reviews (book_isbn, user_id, review, ranking)"
                   "VALUES (:book_isbn, :user_id, :review, :ranking)",
                   {"book_isbn": request.form.get('book_isbn'), "user_id": session.get('user').id,
                    "review": request.form.get('review'), "ranking": request.form.get('rating')})
        db.commit()
        message = {'type': 'success', 'value': f'Review added'}
    except Exception as exception:
        print(exception)
        message = {'type': 'warning', 'value': f'Error while adding review. Try again later'}

    flash(message)
    return redirect(url_for('book', book_isbn=request.form.get('book_isbn')))


@app.route('/api/<int:book_id>')
def book_api(book_id):
    """Return detail about a single book"""

    # Check if flights exist
    # _book = db.query(Book).get(book_id)
    # _book = db.execute(f'SELECT * FROM BOOKS WHERE id == {book_id}')
    # if _book is None:
    #     return jsonify({"error": "invalid book_id"}), 404

    # score = 0
    # for review in _book.review:
    #     score += review.rating
    # review_count = len(_book.review)
    # db.remove()
    #
    # goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
    #                          params={"key": os.getenv('GOODREADS_KEY'), "isbns": _book.isbn})
    # if goodreads.status_code == 200:
    #     goodreads_data = goodreads.json()['books'][0]
    #     review_count += goodreads_data['work_ratings_count']
    #     score += goodreads_data['work_ratings_count'] * float(goodreads_data['average_rating'])
    #
    # if review_count == 0:
    #     score = 0
    # else:
    #     score = float(score) / review_count
    #
    return jsonify({
        "title": "bo",
        "author": "bo",
        "year": "bo",
        "isbn": "bo",
        "review_count": "bo",
        "average_score": "bo",
    }), 200
