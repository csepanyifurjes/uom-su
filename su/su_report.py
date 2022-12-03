import logging
import sqlite3
from contextlib import closing

LOG = logging.getLogger(__name__)


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
                return report
