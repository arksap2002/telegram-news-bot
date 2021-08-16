import pickle
import time

from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from globals import (Article)
import numpy as np
import random


class Neural:
    def __init__(self):
        self.regressor = SGDRegressor(loss='huber', learning_rate='adaptive', eta0=0.5)
        self.samples = []
        self.grades = []
    def partial_fit(self, article_info: Article, grade: float):
        sample = np.array([article_info.likes, article_info.comments, article_info.size, article_info.image_count])
        #sample = [article_info.size]
        self.samples.append(sample)
        self.grades.append(grade)
    def predict(self, article_info: Article):
        sample = np.array([article_info.likes, article_info.comments, article_info.size, article_info.image_count])
        if (len(self.samples) > 0):
            self.regressor.fit(self.samples, self.grades)
            global_model.regressor.fit(self.samples, self.grades)
        return self.regressor.predict(sample)

    def get_best_topics(self, articles):
        grades = []
        for i in articles:
            grades.append((self.predict(i), i))
        return [x[1] for x in sorted(grades)]


def train():
    model = Neural()
    for i in range(1):
        model.partial_fit(Article(0, 0, random.randint(2000, 10000), 0, ""), 10)
        model.partial_fit(Article(0, 0, random.randint(100, 1000), 0, ""), 1)
    for i in range(10):
        size = random.randint(0, 6000)
        print(size, model.predict(Article(0, 0, size, 0, ""))[0])


global_model = Neural()
def global_predict(article: Article):
    return global_model.predict(article)