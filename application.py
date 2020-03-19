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
    print(result)
    if result is None or result == []:
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
        review = db.execute("SELECT * FROM reviews WHERE book_isbn=:isbn AND user_id=:user_id;",
                            {"isbn": request.form.get('book_isbn'), "user_id": session.get('user').id}).fetchmany(1)
        if not review:
            db.execute("INSERT INTO reviews (book_isbn, user_id, review, rating)"
                       "VALUES (:book_isbn, :user_id, :review, :rating)",
                       {"book_isbn": request.form.get('book_isbn'), "user_id": session.get('user').id,
                        "review": request.form.get('review'), "rating": request.form.get('rating')})
            message = {'type': 'success', 'value': f'Review added'}
        else:
            db.execute("UPDATE reviews SET review=:review, rating=:rating WHERE id=:id ",
                       {"id": review[0].id, "review": request.form.get('review'), "rating": request.form.get('rating')})
            message = {'type': 'success', 'value': f'Review updated'}

        db.commit()
    except Exception as exception:
        print(exception)
        message = {'type': 'warning', 'value': f'Error while adding review. Try again later'}

    flash(message)
    return redirect(url_for('book', book_isbn=request.form.get('book_isbn')))


@app.route('/api/<book_isbn>')
def book_api(book_isbn):
    """Return detail about a single book"""

    # Check if book exist
    _book = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": book_isbn}).fetchmany(1)
    if not _book:
        return jsonify({"error": "invalid book_id"}), 404
    else:
        _book = _book[0]

    _review = db.execute("SELECT * FROM reviews WHERE book_isbn=:isbn;",
                         {"isbn": book_isbn}).fetchall()
    score = 0
    for review in _review:
        score += review.rating
    review_count = len(_review)

    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
                             params={"key": os.getenv('GOODREADS_KEY'), "isbns": _book.isbn})
    if goodreads.status_code == 200:
        goodreads_data = goodreads.json()['books'][0]
        review_count += goodreads_data['work_ratings_count']
        score += goodreads_data['work_ratings_count'] * float(goodreads_data['average_rating'])

    if review_count == 0:
        score = 0
    else:
        score = float(score) / review_count

    return jsonify({
        "title": _book.title,
        "author": _book.author,
        "year": _book.year,
        "isbn": _book.isbn,
        "review_count": review_count,
        "average_score": score,
    }), 200


@app.route('/search', methods=['POST', 'GET'])
def search():
    query = []
    if request.method == 'POST':
        query = request.form.get('query').lower()
    elif request.method == 'GET':
        query = request.args.get('query').lower()
    else:
        return redirect(url_for('books'))
    books_filtered = []
    _books = db.execute("SELECT * FROM books;").fetchall()
    for _book in _books:
        if query in {_book.author.lower(), _book.title.lower(), _book.isbn.lower()}:
            books_filtered.append(_book)
    return render_template('books.html', books=books_filtered)
