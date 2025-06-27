from flask_pymongo import PyMongo
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mongo = PyMongo()

def init_db(app):
    logger.debug("Initializing PyMongo with app...")
    mongo.init_app(app)
    logger.debug("PyMongo initialization completed")
