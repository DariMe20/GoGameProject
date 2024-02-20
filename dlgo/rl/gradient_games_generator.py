import os
import h5py
from keras.src.saving.saving_api import load_model
from keras.models import Sequential
from dlgo.agent.policy_agent import PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.goboard import GameState
from dlgo.gotypes import Player
from dlgo.rl.experience_colector import ExperienceCollector
from dlgo.rl import experience


board_size = 9
encoder = SimpleEncoder((board_size, board_size))
model = Sequential()

model_path1 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient2.h5'
model_p1 = load_model(model_path1)

model_path2 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient2.h5'
model_p2 = load_model(model_path2)

agent1 = PolicyAgent(model_p1, encoder)
agent2 = PolicyAgent(model_p2, encoder)

collector1 = ExperienceCollector()
collector2 = ExperienceCollector()

agent1.set_collector(collector1)
agent2.set_collector(collector2)

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
num_episodes = 300

for episode in range(num_episodes):
    collector1.begin_episode()
    collector2.begin_episode()
    print("Started episode: ", episode)

    game_record = play_game(agent1, agent2, board_size)
    if game_record == Player.black:
        collector1.complete_episode(reward=1)
        collector2.complete_episode(reward=-1)
        black_wins += 1
    else:
        collector2.complete_episode(reward=1)
        collector1.complete_episode(reward=-1)
        white_wins += 1
    print(f"Finished episode {episode} with success!")


experience_combined = experience.combine_experience([collector1, collector2])
experience_filename = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\experience_files\\experience21.h5'
with h5py.File(experience_filename, 'w') as experience_outf:
    experience_combined.serialize(experience_outf)

print(f"Black wins: {black_wins} \ {num_episodes} \n White wins: {white_wins} \ {num_episodes}")
# SALVARE MODELE
# model_policy.save('C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\black_agent_model5.h5')
# model_white.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\white_agent_model.h5')

# model.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\model3.h5')
