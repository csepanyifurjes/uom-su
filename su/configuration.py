from su_report import ReportSynergyUnit
from su_explain import ExplainSynergyUnit


class NullSynergyUnit(object):
    """ Object to follow the NULL pattern """

    def __init__(self):
        self.health = "Not implemented"

    def get_health(self):
        return self.health


SYNERGY_UNITS = {
    'report': {
        'class': ReportSynergyUnit
    },
    'explain': {
        'class': ExplainSynergyUnit
    },
    'control': {
        'class': NullSynergyUnit
    },
    'teach': {
        'class': NullSynergyUnit
    },
    'future': {
        'class': NullSynergyUnit
    }
}
