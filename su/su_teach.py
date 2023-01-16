import logging
import sqlite3

import matplotlib.pyplot as plt
import matplotlib
import math

from wordcloud import WordCloud
from su_report import ReportSynergyUnit
from sentence_transformers import SentenceTransformer, util

LOG = logging.getLogger(__name__)


class TeachSynergyUnit(object):
    """ Responsible for teaching the users of the system"""

    def __init__(self):
        self.HEALTH = "UP"
        self.DB = "data/tutor_db.db"
        self.report_su = ReportSynergyUnit()
        self.model = SentenceTransformer('stsb-roberta-large')

    def get_health(self):
        return self.HEALTH

    def teach(self, expected_text, actual_text):
        teaching = {}
        expected = self.model.encode(expected_text, convert_to_tensor=True)
        mask = "<pad>"
        splits = str.split(actual_text)
        for split in splits:
            actual_masked = actual_text.replace(split, mask)
            LOG.debug("actual_masked: " + actual_masked)
            actual = self.model.encode(actual_masked, convert_to_tensor=True)
            cosine_scores = util.pytorch_cos_sim(expected, actual)
            teaching[split] = 1 / 1 - cosine_scores.item()
        return teaching

    def get_teaching_information(self, external_id):
        try:
            report = self.report_su.get_report(external_id)
        except sqlite3.DataError as e:
            raise ValueError('Error while generating teaching: ' + str(e.args[0]))
        teaching = self.teach(report[4], report[4])
        LOG.debug(teaching)
        matplotlib.use('agg')
        wc = WordCloud(width=400, height=400,
                       background_color='white',
                       min_font_size=8).generate_from_frequencies(teaching)
        # plot the WordCloud image
        plt.figure(figsize=(4, 4), facecolor=None)
        plt.imshow(wc)
        plt.axis("off")
        plt.tight_layout(pad=0)
        return plt
