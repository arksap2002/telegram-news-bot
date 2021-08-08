import pickle
import time

from sklearn.linear_model import SGDRegressor
from globals import (Article)
import numpy as np
import random


class Neural:
    def __init__(self):
        self.regressor = SGDRegressor(learning_rate='adaptive', eta0=0.3)

    def partial_fit(self, article_info: Article, grade: int):
        sample = np.array([article_info.likes, article_info.comments, article_info.size, article_info.image_count])
        self.regressor.partial_fit([sample], [grade])

    def predict(self, article_info: Article):
        sample = np.array([article_info.likes, article_info.comments, article_info.size, article_info.image_count])
        return self.regressor.predict([sample])

    def get_best_topics(self, articles):
        grades = []
        for i in articles:
            grades.append((self.predict(i), i))
        return [x[1] for x in sorted(grades)]
