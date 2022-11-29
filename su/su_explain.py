from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib


class ExplainSynergyUnit(object):
    """ Responsible for providing explanation of the executed tasks """

    def __init__(self):
        self.health = "UP"

    def get_health(self):
        return self.health

    def get_explanation(self):
        matplotlib.use('agg')
        wc = WordCloud(width=800, height=800,
                       background_color='white',
                       min_font_size=10).generate_from_text('apple apple apple apple apple banana')
        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wc)
        plt.axis("off")
        plt.tight_layout(pad=0)
        return plt
