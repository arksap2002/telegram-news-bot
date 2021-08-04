import copy
import pickle
import numpy as np
import time
from globals import *


class User:
    def __init__(self):
        self.topics = np.array(TOPICS)
        self.width_of_keyboard = WIDTH_OF_KEYBOARD
        self.mode = MODE
        self.setting_topic_name = SETTINGS_TOPIC_NAME
        # self.neural_network


def load_all_data():
    with open(data_filename, 'rb') as f:
        data = pickle.load(f)
        for key in data.keys():
            all_users[key] = copy.deepcopy(data[key])
        f.close()


def add_to_current_or_create_user(id_: int):
    if id_ not in all_users.keys():
        all_users[id_] = User()
    if id_ not in current_users.keys():
        current_users[id_] = copy.deepcopy(all_users[id_])


def add_theme(id_: int, theme: Topic):
    current_users[id_].topics = np.append(current_users[id_].topics, [theme])


def change_width(id_: int, width: int):
    current_users[id_].width_of_keyboard = width


def remove_theme(id_: int, theme: Topic):
    for i in range(len(current_users[id_].topics)):
        if current_users[id_].topics[i].name == theme.name:
            current_users[id_].topics = np.delete(current_users[id_].topics, i)
            break


def remove_user_from_current(id_: int):
    all_users[id_] = copy.deepcopy(current_users[id_])
    del current_users[id_]


def save_data():
    global curr_time
    if time.time() - curr_time < save_frequency:
        print("now it's not time")
        return
    else:
        print("saving")
        curr_time = time.time()
    for id_ in current_users.keys():
        all_users[id_] = copy.deepcopy(current_users[id_])
    with open(data_filename, 'wb') as f:
        pickle.dump(all_users, f)
        f.close()
