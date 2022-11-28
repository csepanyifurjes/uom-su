from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd


def get_explanation(request_id):
    wc = WordCloud(width=800, height=800,
                   background_color='white',
                   min_font_size=10).generate('apple')
    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


class ExplainSynergyUnit(object):
    """ Responsible for providing explanation of the executed tasks """

    def __init__(self):
        self.health = "UP"

    def get_health(self):
        return self.health
