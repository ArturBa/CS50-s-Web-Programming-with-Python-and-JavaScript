import csv
import os

from flask import Flask

from model import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_PASS"] = os.getenv("DATABASE_PASS")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    f = open("books.csv")
    reader = csv.DictReader(f)
    for row in reader:
        book = Book(isbn=row['isbn'], author=row['author'], title=row['title'], year=row['year'])
        db.session.add(book)
        print(f"Added book: {row['title']} by {row['author']} from {row['year']}")
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
