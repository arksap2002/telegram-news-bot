import pickle
import numpy as np
import time
from globals import *


def load_all_data():
    with open(data_filename, 'rb') as f:
        data = pickle.load(f)
        for key in data.keys():
            all_users[key] = data[key].copy()
        f.close()


def add_to_current_or_create_user(id_: int):
    if id_ not in all_users.keys():
        all_users[id_] = np.array(TOPICS)
    if id_ not in current_users.keys():
        current_users[id_] = np.array(all_users[id_])


def add_theme(id_: int, theme: Topic):
    current_users[id_] = np.append(current_users[id_], [theme])


def remove_theme(id_: int, theme: Topic):
    for i in range(len(current_users[id_])):
        if current_users[id_][i].name == theme.name:
            current_users[id_] = np.delete(current_users[id_], i)
            break


def remove_user_from_current(id_: int):
    all_users[id_] = np.array(current_users[id_])
    del current_users[id_]


def save_data():
    if (time.time() - curr_time < save_frequency):
        print("now it's not time")
        return
    else:
        print("saving")
        curr_time.__add__(time.time() - curr_time)
    for id_ in current_users.keys():
        all_users[id_] = np.array(current_users[id_])
    with open(data_filename, 'wb') as f:
        pickle.dump(all_users, f)
        f.close()
