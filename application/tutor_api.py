import logging
import sqlite3

from contextlib import closing
from flask import Flask, jsonify


LOG = logging.getLogger(__name__)

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


@app.get("/tutor/health")
def get_health():
    LOG.info("Health check of tutor has been requested")
    return jsonify("UP")


@app.get("/tutor/questions")
def get_questions():
    LOG.info("Available questions have been requested")
    with closing(sqlite3.connect("../data/tutor_db.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT * from questions")
            return jsonify(cursor.fetchall())

