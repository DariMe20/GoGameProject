import h5py
import keras
import numpy as np
import tensorflow as tf

from keras.src.regularizers import l2
from keras.src.saving.saving_api import load_model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import Adam

from dlgo import agent, rl
from dlgo.agent import policy_agent
from dlgo.agent.policy_agent import PolicyAgent
from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.goboard import GameState
from dlgo.gotypes import Player
from dlgo.keras_networks import large_network
from dlgo.rl.experience_colector import ExperienceCollector
from dlgo.rl import experience


board_size = 9
encoder = SimpleEncoder((board_size, board_size))
model = Sequential()

model_path = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\black_agent_model3.h5'
model_p = load_model(model_path)

agent1 = PolicyAgent(model_p, encoder)
agent2 = PolicyAgent(model_p, encoder)

collector1 = ExperienceCollector()
collector2 = ExperienceCollector()

agent1.set_collector(collector1)
agent2.set_collector(collector2)

# METODA PENTRU JOC SI COLECTARE A EXPERIENTELOR
def play_game(agent_black, agent_white, board_size):
    state = GameState.new_game(board_size)
    agents = {
        Player.black: agent_black,
        Player.white: agent_white
    }
    last_num_prisoners = 0

    while not state.is_over():
        next_player = state.next_player
        agent_next = agents[next_player]
        move = agent_next.select_move(state)
        state = state.apply_move(move)
    return state.winner()



# SETAREA NUMARULUI DE EPISOADE SI APELAREA METODELOR DE ANTRENARE
num_episodes = 10

for episode in range(num_episodes):
    collector1.begin_episode()
    collector2.begin_episode()
    print("Started episode: ", episode)

    game_record = play_game(agent1, agent2, board_size)
    if game_record == Player.black:
        collector1.complete_episode(reward=1)
        collector2.complete_episode(reward=-1)
    else:
        collector2.complete_episode(reward=1)
        collector1.complete_episode(reward=-1)
    print(f"Finished episode {episode} with success!")


experience = experience.combine_experience([collector1,collector2])
experience_filename = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\experience_files\\experience1.h5'
with h5py.File(experience_filename, 'w') as experience_outf:
    experience.serialize(experience_outf)

# SALVARE MODELE
# model_policy.save('C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\black_agent_model5.h5')
# model_white.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\white_agent_model.h5')

# model.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\model3.h5')

