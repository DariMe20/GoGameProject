from keras import Sequential
from keras.src.saving.saving_api import load_model

import MonteCarloTreeSearch.MCTS
from dlgo.agent import RandomBot, PolicyAgent, DeepLearningAgent
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

path_DL = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model2.h5'
model_DL = load_model(path_DL)

# BOT INITIALIZERS
RANDOM_BOT = RandomBot()
MCTS_BOT = MonteCarloTreeSearch.MCTS.MCTSAgent(model, oneplane)
PG_1 = PolicyAgent(model_pg1, encoder)
PG_2 = PolicyAgent(model_pg2, encoder)
PG_3 = PolicyAgent(model_pg3, encoder)
PG_4 = PolicyAgent(model_pg4, encoder)
DL_BOT = DeepLearningAgent(model_DL, oneplane)

# DICTIONARY FOR BOTS
BOTS = {
    "Random Bot": RANDOM_BOT,
    "MCTS": MCTS_BOT,
    "Policy Gradient 1": PG_1,
    "Policy Gradient 2": PG_2,
    "Policy Gradient 3": PG_3,
    "Policy Gradient 4": PG_4,
    "DL Prediction Bot": DL_BOT
}
