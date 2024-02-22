import os
import h5py
from keras.src.saving.saving_api import load_model
from keras.models import Sequential

from dlgo import utils
from dlgo.agent.policy_agent import PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.goboard import GameState
from dlgo.gotypes import Player
from dlgo.rl.experience_colector import ExperienceCollector
from dlgo.rl import experience
from utils import constants

agent1 = constants.BOTS['Policy Gradient 3']
agent2 = constants.BOTS['DL Prediction Bot']

collector1 = ExperienceCollector()
collector2 = ExperienceCollector()

agent1.set_collector(collector1)
# agent2.set_collector(collector2)

black_wins = 0
white_wins = 0


# METODA PENTRU JOC SI COLECTARE A EXPERIENTELOR
def play_game(agent_black, agent_white, board_size):
    state = GameState.new_game(board_size)
    agents = {
        Player.black: agent_black,
        Player.white: agent_white
    }

    while not state.is_over():
        next_player = state.next_player
        agent_next = agents[next_player]
        move = agent_next.select_move(state)
        state = state.apply_move(move)
    return state.winner()



# SETAREA NUMARULUI DE EPISOADE SI APELAREA METODELOR DE ANTRENARE
num_episodes = 100

for episode in range(num_episodes):
    collector1.begin_episode()
    # collector2.begin_episode()
    print("Started episode: ", episode)

    game_record = play_game(agent1, agent2, 9)
    if game_record == Player.black:
        collector1.complete_episode(reward=1)
        # collector2.complete_episode(reward=-1)
        black_wins += 1
    else:
        # collector2.complete_episode(reward=1)
        collector1.complete_episode(reward=-1)
        white_wins += 1
    print(f"Finished episode {episode} with success!")


experience_combined = experience.combine_experience([collector1])
experience_filename = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\experience_files\\experience36.h5'
with h5py.File(experience_filename, 'w') as experience_outf:
    experience_combined.serialize(experience_outf)

print(f"Black wins: {black_wins} \ {num_episodes} \n White wins: {white_wins} \ {num_episodes}")
