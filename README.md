# Project 1

Web Programming with Python and JavaScript

This is a website for a reviewing books.

### Requirements
- Install python required packages
```shell script
pip install -r requirements.txt
```
- Set up environment variables:
    - DATABASE_URL
    - DATABASE_PASS
    - GOODREADS_KEY
 - For additional security you can set up environment variable 
    - SALT (used to generate even more secure password hashes)
    
### Toolchain:
- Python: Flask
- HTML5/SASS 
- POSTGRESQL

### API:
**Get book statistics a given ISBN**

Get review statistics for books by a given ISBN. 
- URL: `/api/isbn` 
- Example:  `/api/1595543414`
- HTTP method: GET
- Parameters:
    -  isbn: Book ISBN


### Files:
- import.py – import data from books.csv to database
- drop_db.py – delete all tables in database
- create_db.py – create all require tables in database
- application.py – flask web server
- utils.py – functions for codding password
- requirements.txt – packages required by python for this project
- templates/* – web-pages to show end user
- static/* – css files for proper formatting a web-page