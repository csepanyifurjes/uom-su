import logging
import sqlite3

import matplotlib.pyplot as plt
import matplotlib

from wordcloud import WordCloud
from su_report import ReportSynergyUnit
from sentence_transformers import SentenceTransformer, util

LOG = logging.getLogger(__name__)


class ExplainSynergyUnit(object):
    """ Responsible for providing explanation of the executed tasks """

    def __init__(self):
        self.HEALTH = "UP"
        self.DB = "data/tutor_db.db"
        self.report_su = ReportSynergyUnit()
        # self.model = SentenceTransformer('stsb-roberta-large')
        self.model = SentenceTransformer('NYTK/sentence-transformers-experimental-hubert-hungarian')

    def get_health(self):
        return self.HEALTH

    def explain(self, expected_text, actual_text, score):
        explanation = {}
        expected = self.model.encode(expected_text, convert_to_tensor=True)
        mask = "<mask>"
        splits = str.split(actual_text)
        for split in splits:
            actual_masked = actual_text.replace(split, mask)
            LOG.debug("actual_masked: " + actual_masked)
            actual = self.model.encode(actual_masked, convert_to_tensor=True)
            cosine_scores = util.pytorch_cos_sim(expected, actual)
            explanation[split] = abs(cosine_scores.item())
        return explanation

    def get_explanation(self, external_id):
        try:
            report = self.report_su.get_report(external_id)
        except sqlite3.DataError as e:
            raise ValueError('Error while generating explanation: ' + str(e.args[0]))
        explanation = self.explain(report[4], report[5], report[6])
        LOG.debug(explanation)
        matplotlib.use('agg')
        wc = WordCloud(width=400, height=400,
                       background_color='white',
                       min_font_size=7).generate_from_frequencies(explanation)
        # plot the WordCloud image
        plt.figure(figsize=(4, 4), facecolor=None)
        plt.imshow(wc)
        plt.axis("off")
        plt.tight_layout(pad=0)
        return plt
