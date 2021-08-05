import time

from sklearn.linear_model import SGDRegressor
from globals import (Article, ENCODER)
from loading import load_topics
import numpy as np
import random

class Neural:
    def __init__(self):
        self.regressor = SGDRegressor(learning_rate='adaptive', eta0=0.2)

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

def train():
    load_topics()
    model = Neural()
    for i in range(10):
        model.partial_fit(Article("Self", random.random()*1000, random.random()*100, random.random()*10+3), 10)
        model.partial_fit(Article("TV", random.random()*1000, random.random()*100, random.random()*10+3), 1)

        print("Self", model.predict(Article("Self", 100, 1, 6)))
        print("TV", model.predict(Article("TV", 100, 1, 6)))
        print("Race", model.predict(Article("Race", 100, 1, 6)))
        time.sleep(0.1)
    for i in range(10):
        model.partial_fit(Article("Music", random.random()*1000, random.random()*100, random.random()*10+3), 10)
        model.partial_fit(Article("Race", random.random()*1000, random.random()*100, random.random()*10+3), 1)

        print("Self", model.predict(Article("Self", 100, 1, 6)))
        print("Music", model.predict(Article("Music", 100, 1, 6)))
        print("Race", model.predict(Article("Race", 100, 1, 6)))
        time.sleep(0.1)