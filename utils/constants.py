import os

from keras import Sequential
from keras.src.saving.saving_api import load_model

from agent import RandomBot, PolicyAgent, DeepLearningAgent, QAgent
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


path_pg1 = os.path.join(gradient_descent_models_dir(), 'model_gradient1.h5')
model_pg1 = load_model(path_pg1)

path_pg2 = os.path.join(gradient_descent_models_dir(), 'model_gradient1.h5')
model_pg2 = load_model(path_pg2)

path_pg3 = os.path.join(gradient_descent_models_dir(), 'model_gradient1.h5')
model_pg3 = load_model(path_pg3)

path_pg4 = os.path.join(gradient_descent_models_dir(), 'model_gradient1.h5')
model_pg4 = load_model(path_pg4)

path_pg5 = os.path.join(gradient_descent_models_dir(), 'model_gradient1.h5')
model_pg5 = load_model(path_pg5)

path_DL = os.path.join(gradient_descent_models_dir(), 'model_PredictionAgent.h5')
model_DL = load_model(path_DL)

path_Q1 = os.path.join(q_models_dir(), 'model_Q1.h5')
model_Q1 = load_model(path_Q1)

path_Q2 = os.path.join(q_models_dir(), 'model_Q2.h5')
model_Q2 = load_model(path_Q2)

path_Q2_V2 = os.path.join(q_models_dir(), 'model_Q2_V2.h5')
model_Q2_V2 = load_model(path_Q2_V2)

# BOT INITIALIZERS
RANDOM_BOT = RandomBot()
PG_1 = PolicyAgent(model_pg1, encoder)
PG_2 = PolicyAgent(model_pg2, encoder)
PG_3 = PolicyAgent(model_pg3, encoder)
PG_4 = PolicyAgent(model_pg4, encoder)
PG_5 = PolicyAgent(model_pg5, encoder)
DL_BOT = DeepLearningAgent(model_DL, oneplane)
Q1 = QAgent(model_Q1, encoder)
Q2 = QAgent(model_Q2, encoder)
Q2_V2 = QAgent(model_Q2_V2, encoder)

# DICTIONARY FOR BOTS
BOTS = {
    "Random Bot": RANDOM_BOT,
    "Policy Gradient 1": PG_1,
    "Policy Gradient 2": PG_2,
    "Policy Gradient 3": PG_3,
    "Policy Gradient 4": PG_4,
    "Policy Gradient 5": PG_5,
    "DL Prediction Bot": DL_BOT,
    "Q1": Q1,
    "Q2": Q2,
    "Q2_v2": Q2_V2
    }
