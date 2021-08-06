import pickle
import time

from sklearn.linear_model import SGDRegressor
from globals import (Article, ENCODER, load_topics, ALL_TOPICS)
import numpy as np
import random


class Neural:
    def __init__(self):
        self.regressor = SGDRegressor(learning_rate='adaptive', eta0=0.05)
        with open('../default_neural.pkl', 'rb') as f:
            self.regressor = pickle.load(f)
            self.regressor.eta0 = 0.15

    def partial_fit(self, article_info: Article, grade: int):
        sample = ENCODER.transform([[article_info.topic]])
        sample = np.append(sample, [1.0 / (article_info.likes + 1), 1.0 / (article_info.comments + 1),
                                    1.0 / (article_info.read_time + 1)])
        self.regressor.partial_fit([sample], [grade])

    def predict(self, article_info: Article):
        sample = ENCODER.transform([[article_info.topic]])
        sample = np.append(sample, [1.0 / (article_info.likes + 1), 1.0 / (article_info.comments + 1),
                                    1.0 / (article_info.read_time + 1)])
        return self.regressor.predict([sample])

    def get_best_topics(self, articles):
        grades = []
        for i in articles:
            grades.append((self.predict(i), i))
        return [x[1] for x in sorted(grades)]


def train():
    load_topics()
    model = Neural()
    for i in range(1000):
        sample = Article(ALL_TOPICS[random.randint(0, len(ALL_TOPICS) - 1)][0], random.randint(0, 10000),
                         random.randint(0, 200), random.randint(2, 10))
        model.partial_fit(sample, sample.likes / 2000 + sample.comments / 100)
    with open('default_neural.pkl', 'wb') as f:
        pickle.dump(model, f)
