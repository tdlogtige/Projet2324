import os
import logging
import pymongo
from pymongo import MongoClient

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def init_db():
    if os.getenv("IS_UNIT_TESTING") == "True":
        logging.info("Unit testing, not initializing database")
        return
    logging.info("Initializing database")
    try:
        database_name = 'db'
        client = MongoClient(
            host="151.80.56.147",  # Adresse IP du serveur MongoDB
            port=27017,
            username=os.getenv("MONGO_USERNAME"),
            password=os.getenv("MONGO_PASSWORD"),
            authSource="admin"
        )
        db = client[database_name]
        logging.info('Connected to MongoDB')
    except pymongo.errors.ConnectionFailure as e:
        logging.error('Could not connect to MongoDB: %s', e)
        exit(1)
    logging.info("Database initialized")
    return db

db = init_db()