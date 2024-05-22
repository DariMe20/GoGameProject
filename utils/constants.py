import os

from keras import Sequential
from keras.src.saving.saving_api import load_model

from agent import RandomBot, PolicyAgent, QAgent
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

path_pg2_1 = os.path.join(gradient_descent_models_dir(), 'NO2_1_model_Gradient.h5')
model_pg2_1 = load_model(path_pg2_1)

path_pg3 = os.path.join(gradient_descent_models_dir(), 'NO3_model_Gradient.h5')
model_pg3 = load_model(path_pg3)

path_Q1 = os.path.join(q_models_dir(), 'Model1_QValue.h5')
model_Q1 = load_model(path_Q1)

path_Q2 = os.path.join(q_models_dir(), 'Model2_QValue.h5')
model_Q2 = load_model(path_Q2)

path_Q3 = os.path.join(q_models_dir(), 'Model3_QValue.h5')
model_Q3 = load_model(path_Q3)

# BOT INITIALIZERS
RANDOM_BOT = RandomBot()
PG_1 = PolicyAgent(model_pg1, encoder)
PG_2 = PolicyAgent(model_pg2, encoder)
PG_2_1 = PolicyAgent(model_pg2_1, encoder)
PG_3 = PolicyAgent(model_pg3, encoder)
Q_1 = QAgent(model_Q1, encoder)
Q_2 = QAgent(model_Q2, encoder)
Q_3 = QAgent(model_Q3, encoder)

# DICTIONARY FOR BOTS
BOTS = {
    "Random Bot": RANDOM_BOT,
    "Policy Gradient 1": PG_1,
    "Policy Gradient 2": PG_2,
    "Policy Gradient Intermediate": PG_2_1,
    "Policy Gradient 3": PG_3,
    "QValue 1": Q_1,
    "QValue 2": Q_2,
    "QValue 3": Q_3
    }
