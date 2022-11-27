import logging
import sqlite3

from contextlib import closing
from sentence_transformers import SentenceTransformer, util

LOG = logging.getLogger(__name__)
DB = "data/tutor_db.db"

MODEL = SentenceTransformer('stsb-roberta-large')

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


def get_questions():
    sql_get_questions = "SELECT question_id, question_text from questions"
    LOG.debug("Executing: [%s]", sql_get_questions, exc_info=1)
    with closing(sqlite3.connect(DB)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql_get_questions)
            return cursor.fetchall()


def get_question(question_id):
    sql_get_question_by_id = f"SELECT question_text from questions where question_id = {question_id}"
    LOG.debug("Executing: [%s]", sql_get_question_by_id, exc_info=1)
    with closing(sqlite3.connect(DB)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql_get_question_by_id)
            return cursor.fetchone()


def get_answer(question_id):
    sql_get_answer_by_id = f"SELECT answer_text from questions where question_id = {question_id}"
    LOG.debug("Executing: [%s]", sql_get_answer_by_id, exc_info=1)
    with closing(sqlite3.connect(DB)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql_get_answer_by_id)
            answer = cursor.fetchone()[0]
            LOG.debug(answer)
            return answer


def evaluate_learners_answer(question_id, learners_answer):
    LOG.debug("question_id: [%s] learners_answer: [%s]", question_id, learners_answer, exc_info=1)
    expected_answer = get_answer(question_id)
    if expected_answer != "":
        LOG.debug("Expected: [%s] Actual: [%s]", expected_answer, learners_answer, exc_info=1)
        expected = MODEL.encode(expected_answer, convert_to_tensor=True)
        actual = MODEL.encode(learners_answer, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(expected, actual)
        return cosine_scores.item()
    LOG.debug("The provided question_id does not exist in the database!")
    return -1
