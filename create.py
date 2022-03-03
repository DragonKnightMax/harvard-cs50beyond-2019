from models import *
from flask import Flask
from dotenv import load_dotenv
import logging, os

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    try:
        db.create_all()
        logger.info("Table schemas created")
    except:
        logger.error("Something went wrong when creating table schemas")

if __name__ == "__main__":
    with app.app_context():
        main()