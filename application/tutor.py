import logging
import sqlite3

from contextlib import closing


LOG = logging.getLogger(__name__)
DB = "data/tutor_db.db"
SQL_GET_QUESTIONS = "SELECT * from questions"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


def get_questions():
    with closing(sqlite3.connect(DB)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(SQL_GET_QUESTIONS)
            return cursor.fetchall()
