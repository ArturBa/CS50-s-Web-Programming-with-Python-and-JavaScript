import requests
from flask import Flask, session, render_template, jsonify, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

from model import *
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
    if session.get('logged'):
        return render_template('user.html', user=session.get('user'))
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
        _user = User(username=post_username, password=post_password, name=post_name)
        db()
        db.add(_user)
        db.commit()
        db.remove()
        message = {'type': 'success', 'value': 'User created'}
        flash(message)
        return redirect(url_for('login'))
    except exc.IntegrityError:
        message = {'type': 'warning', 'value': 'User with that username already exist'}
        flash(message)
        return redirect(url_for('register'))


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    session['logged'] = False
    return redirect(url_for('index'))


@app.route('/login_authorization', methods=['POST'])
def login_authorization():
    if request.method != 'POST':
        message = {'type': 'warning', 'value': f'{request.method} is not POST\nWrong method used'}
        flash(message)
        return redirect(url_for('login'))
    post_username = str(request.form.get('username'))
    post_password = code_password(str(request.form.get('password')))

    db()
    query = db.query(User).filter(User.username.in_([post_username]), User.password.in_([post_password]))
    db.remove()
    result = query.first()
    if result is None:
        message = {'type': 'warning', 'value': 'Login and password not matching'}
        flash(message)
        return redirect(url_for('login'))
    else:
        session['logged'] = True
        session['user'] = result
        return redirect(url_for('index'))


@app.route('/books')
def books():
    """Return detail about all books"""
    _books = db.query(Book).all()
    return render_template("books.html", books=_books)


@app.route('/book/<int:book_id>')
def book(book_id):
    """Return detail about a single book"""
    try:
        _book = db.query(Book).get(book_id)
        goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
                                 params={"key": os.getenv('GOODREADS_KEY'), "isbns": _book.isbn})
        if goodreads.status_code == 200:
            goodreads_data = goodreads.json()['books'][0]
        else:
            goodreads_data = None
        if session.get('logged'):
            _user = session.get('user')
        else:
            _user = None
        return render_template("book.html", user=_user, book=_book, goodreads=goodreads_data)
    except Exception as exception:
        print(type(exception))
        return render_template("error.html", message="Book not found")


@app.route('/add_opinion', methods=['POST'])
def add_opinion():
    if request.method != 'POST':
        return redirect(url_for('index'))
    try:
        review = Review(user_id=session.get('user').id, book_id=request.form.get('book_id'),
                        rating=request.form.get('rating'), review=request.form.get('review'))
        db()
        db.add(review)
        db.commit()
        db.remove()
        message = {'type': 'success', 'value': f'Review added'}
    except Exception as exception:
        print(exception)
        message = {'type': 'warning', 'value': f'Error while adding review. Try again later'}

    flash(message)
    return redirect(url_for('book', book_id=request.form.get('book_id')))


@app.route('/api/<int:book_id>')
def book_api(book_id):
    """Return detail about a single book"""

    # Check if flights exist
    db()
    _book = db.query(Book).get(book_id)
    if _book is None:
        return jsonify({"error": "invalid book_id"}), 404

    score = 0
    for review in _book.review:
        score += review.rating
    review_count = len(_book.review)
    db.remove()

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

    # Get passengers
    return jsonify({
        "title": _book.title,
        "author": _book.author,
        "year": _book.year,
        "isbn": _book.isbn,
        "review_count": review_count,
        "average_score": score
    }), 200
