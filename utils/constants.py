from keras import Sequential
from keras.src.saving.saving_api import load_model

from dlgo.agent import RandomBot, PolicyAgent, DeepLearningAgent, QAgent
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.encoders.simple import SimpleEncoder

board_size = 9
encoder = SimpleEncoder((board_size, board_size))
oneplane = OnePlaneEncoder((board_size, board_size))
model = Sequential()

path_pg1 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient1.h5'
model_pg1 = load_model(path_pg1)

path_pg2 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient2.h5'
model_pg2 = load_model(path_pg2)

path_pg3 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient3.h5'
model_pg3 = load_model(path_pg3)

path_pg4 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient4.h5'
model_pg4 = load_model(path_pg4)

path_pg5 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient5.h5'
model_pg5 = load_model(path_pg5)

path_DL = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model2.h5'
model_DL = load_model(path_DL)

path_Q1 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_models\\model_Q1.h5'
model_Q1 = load_model(path_Q1)

path_Q2 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_models\\model_Q2.h5'
model_Q2 = load_model(path_Q2)


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
    "Q2": Q2
    }
