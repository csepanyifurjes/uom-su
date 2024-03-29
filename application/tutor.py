import logging
import sqlite3
import uuid

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
            result = cursor.fetchone()
            if not result:
                raise sqlite3.DataError('The provided question id can not be found in DB!')
            answer = result[0]
            LOG.debug(answer)
            return answer


def persist_report(question_id, expected_answer, learners_answer, score, client_info, grade_group_id, grade_text):
    report_external_id = uuid.uuid4()
    learners_answer = learners_answer.replace("'", "`")
    sql_insert_report = f"INSERT INTO report(report_external_id," \
                        f" question_id, expected_answer, learners_answer, score, client_info, grade_group_id,  " \
                        f"grade_text) VALUES ('{report_external_id}'," \
                        f"{question_id}, '{expected_answer}', '{learners_answer}', {score}, '{client_info}', " \
                        f"{grade_group_id}, '{grade_text}')"
    LOG.debug("Executing: [%s]", sql_insert_report, exc_info=1)
    with closing(sqlite3.connect(DB)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql_insert_report)
            connection.commit()
            return report_external_id


def get_grade(score):
    sql_get_grade_by_score = f"SELECT grade_group_id, grade_text FROM grade WHERE grade_group_id = " \
                             f"(select config_value from config " \
                             f"where config_key = 'grade_group') AND range_start <= {score}" \
                             f" ORDER BY range_start DESC LIMIT 1"
    LOG.debug("Executing: [%s]", sql_get_grade_by_score, exc_info=1)
    with closing(sqlite3.connect(DB)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql_get_grade_by_score)
            return cursor.fetchone()


def evaluate_learners_answer(question_id, learners_answer, client_info):
    LOG.debug("question_id: [%s] learners_answer: [%s]", question_id, learners_answer, exc_info=1)
    try:
        expected_answer = get_answer(question_id)
    except sqlite3.DataError as e:
        raise ValueError("Can not evaluate learner's answer: " + e.args[0])
    if expected_answer != "":
        LOG.debug("Expected: [%s] Actual: [%s]", expected_answer, learners_answer, exc_info=1)
        expected = MODEL.encode(expected_answer, convert_to_tensor=True)
        actual = MODEL.encode(learners_answer, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(expected, actual)
        grade_group_id, grade_text = get_grade(cosine_scores.item())
        external_id = persist_report(question_id, expected_answer, learners_answer, cosine_scores.item(),
                                     client_info, grade_group_id, grade_text)
        return external_id, grade_text, cosine_scores.item()
    LOG.debug("The provided question_id does not exist in the database!")
    return -1, "unknown"
