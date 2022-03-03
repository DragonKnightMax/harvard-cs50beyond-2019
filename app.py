from pydoc import render_doc
from flask import Flask, render_template, request, url_for, redirect, flash
from models import *
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        author_or_title = request.form.get("search")
        if not author_or_title:
            msg = "Author or Title must not be empty"
            flash(msg)
            return render_template("error.html", msg=msg)
        
        like_clause = f"%{author_or_title}%"
        books = Book.query.filter(Book.title.ilike(like_clause)).all()
        if books is None:
            flash("No matching book")
            books = []
        
        authors = Author.query.filter(Author.name.ilike(like_clause)).all()
        if authors is None:
            flash("No matching author")
            authors = []
        
        return render_template("result.html", search=author_or_title, books=books, authors=authors)
    
    else:
        return render_template("search.html")


@app.route("/author/<int:id>")
def author(id):
    a = Author.query.filter_by(id=id).first()
    if a is None:
        msg = "Author does not exist in database!"
        flash(msg)
        return render_template("error.html", msg=msg)
    return render_template("author.html", author=a)


@app.route("/book/<string:isbn>")
def book(isbn):
    b = Book.query.filter_by(isbn=isbn).first()
    if b is None:
        msg = "Book does not exist in database!"
        flash(msg)
        return render_template("error.html", msg=msg)
    return render_template("book.html", book=b)
