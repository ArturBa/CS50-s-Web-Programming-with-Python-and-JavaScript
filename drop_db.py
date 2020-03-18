import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    db.execute("DROP TABLE IF EXISTS books;")
    db.execute("DROP TABLE IF EXISTS users;")
    db.execute("DROP TABLE IF EXISTS reviews;")
    db.commit()


if __name__ == "__main__":
    main()
