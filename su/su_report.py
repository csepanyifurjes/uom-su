import logging
import sqlite3
from contextlib import closing

LOG = logging.getLogger(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ReportSynergyUnit(object):
    """ Responsible for providing information about the executed tasks as well as some statistical data"""

    def __init__(self):
        self.HEALTH = "UP"
        self.DB = "data/tutor_db.db"

    def get_health(self):
        return self.HEALTH

    def get_report(self, report_external_id):
        sql_get_report_by_external_id = f"SELECT * from report where report_external_id = '{report_external_id}'"
        LOG.debug("Executing: [%s]", sql_get_report_by_external_id, exc_info=1)
        with closing(sqlite3.connect(self.DB)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(sql_get_report_by_external_id)
                report = cursor.fetchone()
                LOG.debug(report)
                if not report:
                    raise sqlite3.DataError('The provided external_id can not be found in DB!')
                return report

    def get_stat(self):
        sql_get_stat = f"SELECT question_id as question, COUNT(question_id) as question_asked, AVG(score) as score_avg, " \
                       f"MIN(score) as score_min, MAX(score) as score_max FROM report " \
                       f"GROUP BY question_id"
        LOG.debug("Executing: [%s]", sql_get_stat, exc_info=1)
        with closing(sqlite3.connect(self.DB)) as connection:
            connection.row_factory = dict_factory
            with closing(connection.cursor()) as cursor:
                cursor.execute(sql_get_stat)
                report = cursor.fetchall()
                LOG.debug(report)
                if not report:
                    raise sqlite3.DataError('Can not fetch statistical information from DB!')
                return report
