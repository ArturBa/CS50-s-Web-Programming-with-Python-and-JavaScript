from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    review = db.relationship("Review", backref="Book", lazy=True)

    def add_review(self, user, rating, review):
        r = Review(user=user, book=self, rating=rating, review=review)
        db.session.add(r)
        db.session.commit(r)

    def __str__(self):
        return f"Book: {self.title} by {self.author}"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    review = db.relationship("Review", backref="User", lazy=True)

    def add_review(self, book, rating, review):
        r = Review(user=self, book=book, rating=rating, review=review)
        db.session.add(r)
        db.session.commit(r)

    def get_opinion(self, book):
        return Review.query.filterby(book_id=book.id, user_id=self.id)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
