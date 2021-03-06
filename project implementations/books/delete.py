from flask import Flask
from models import *
import os, logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    try:
        db.drop_all()
        logger.info("Dropped all tables in database")
    except:
        logger.error("Failed to drop tables in database")

if __name__ == "__main__":
    with app.app_context():
        main()