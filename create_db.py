import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    db.execute("CREATE TABLE books ("
               "isbn VARCHAR PRIMARY KEY, "
               "title VARCHAR NOT NULL, "
               "author VARCHAR NOT NULL, "
               "year INTEGER NOT NULL);"
               )
    db.execute("CREATE TABLE users ("
               "id SERIAL PRIMARY KEY, "
               "username VARCHAR UNIQUE NOT NULL, "
               "password VARCHAR NOT NULL, "
               "name VARCHAR NOT NULL);"
               )
    db.execute("CREATE TABLE reviews ("
               "id SERIAL PRIMARY KEY, "
               "book_id SERIAL NOT NULL, "
               "user_id SERIAL NOT NULL, "
               "review VARCHAR NOT NULL, "
               "value VARCHAR NOT NULL);"
               )
    db.commit()


if __name__ == "__main__":
    main()
