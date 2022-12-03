import logging
import sqlite3

from contextlib import closing
from enum import Enum


LOG = logging.getLogger(__name__)


class GradeGroup(Enum):
    TEXTUAL = 1
    BINARY = 2
    SCHOOLISH = 3


class ControlSynergyUnit(object):
    """ Responsible for controlling the behaviour of the application"""

    def __init__(self):
        self.HEALTH = "UP"
        self.DB = "data/tutor_db.db"

    def get_health(self):
        return self.HEALTH

    def update_grade_group(self, grade_group):
        try:
            grade_group_id = GradeGroup[grade_group].value
        except KeyError:
            return [member.name for member in GradeGroup]
        sql_update_grade_group_config = f"update config set config_value='{grade_group_id}' " \
                                        f"where config_key = 'grade_group'"
        LOG.debug("Executing: [%s]", sql_update_grade_group_config, exc_info=1)
        with closing(sqlite3.connect(self.DB)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(sql_update_grade_group_config)
                connection.commit()
                return "OK"

