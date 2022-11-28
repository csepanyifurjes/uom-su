class ReportSynergyUnit(object):
    """ Responsible for providing information about the executed tasks """

    def __init__(self):
        self.health = "UP"

    def get_health(self):
        return self.health

