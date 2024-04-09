import os

from keras import Sequential
from keras.src.saving.saving_api import load_model

from agent import RandomBot, PolicyAgent
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.encoders.simple import SimpleEncoder

board_size = 9
encoder = SimpleEncoder((board_size, board_size))
oneplane = OnePlaneEncoder((board_size, board_size))
model = Sequential()


def base_dir():
    return os.path.join('..', '..', 'reinforcement_learning')


def gradient_descent_models_dir():
    return os.path.join(base_dir(), 'gradient_descent', 'gradient_descent_models')


def q_models_dir():
    return os.path.join(base_dir(), 'q_value', 'q_models')


path_pg1 = os.path.join(gradient_descent_models_dir(), 'NO1_model_Gradient.h5')
model_pg1 = load_model(path_pg1)

path_pg2 = os.path.join(gradient_descent_models_dir(), 'NO2_model_Gradient.h5')
model_pg2 = load_model(path_pg2)

# BOT INITIALIZERS
RANDOM_BOT = RandomBot()
PG_1 = PolicyAgent(model_pg1, encoder)
PG_2 = PolicyAgent(model_pg2, encoder)

# DICTIONARY FOR BOTS
BOTS = {
    "Random Bot": RANDOM_BOT,
    "Policy Gradient 1": PG_1,
    "Policy Gradient 2": PG_2,
    }
