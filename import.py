from sqlalchemy.exc import IntegrityError
from flask import Flask
from models import *
import csv, os, logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)  # skip csv header
    row = 0
    for isbn, title, author, year in reader:
        a = Author(name=author)
        try:
            db.session.add(a)
            db.session.commit()
            logger.info(f"Added Author: {author}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Author already exist: {author}")

        a = Author.query.filter_by(name=author).first()
        if a is None:
            logger.error("Author does not exist")
            return
        
        try:
            a.addBook(isbn=isbn, title=title, year=year)
            logger.info(f"Added Book: {title}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Book already exist: {title}")
        
        row += 1
        logger.info(f"Row {row}")

    db.session.commit()
    logger.info("Books dataset loaded into database")

if __name__ == "__main__":
    with app.app_context():
        main()