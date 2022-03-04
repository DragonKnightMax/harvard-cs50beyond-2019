from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    books = db.relationship("Book", back_populates="author")

    def addBook(self, isbn, title, year):
        b = Book(isbn=isbn, title=title, year=year, author_id=self.id)
        db.session.add(b)
        db.session.commit()
        

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    year = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    author = db.relationship("Author", back_populates="books")