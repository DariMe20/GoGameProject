import h5py
from keras import Sequential
from keras.src.saving.saving_api import load_model

from dlgo.agent import QAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.goboard import GameState
from dlgo.gotypes import Player
from dlgo.rl import experience
from dlgo.rl.experience_colector import ExperienceCollector

board_size = 9
encoder = SimpleEncoder((board_size, board_size))
model = Sequential()

path_Q1 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_models\\model_Q1.h5'
model_Q1 = load_model(path_Q1)
path_Q2 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_models\\model_Q1.h5'
model_Q2 = load_model(path_Q2)

agent1 = QAgent(model_Q1, encoder)
agent2 = QAgent(model_Q2, encoder)

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
num_episodes = 100

for episode in range(num_episodes):
    print("Started episode: ", episode)
    collector1.begin_episode()
    collector2.begin_episode()

    game_record = play_game(agent1, agent2, 9)
    if game_record == Player.black:
        collector1.complete_episode(reward=1)
        collector2.complete_episode(reward=-1)
        black_wins += 1
    else:
        collector2.complete_episode(reward=1)
        collector1.complete_episode(reward=-1)
        white_wins += 1
    print(f"Finished episode {episode} with success!")


experience1 = experience.combine_experience([collector1])
experience2 = experience.combine_experience([collector2])
experience_filename1 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_value_experience_files\\Q_experience2.h5'
with h5py.File(experience_filename1, 'w') as experience_outf:
    experience2.serialize(experience_outf)

print(f"Black wins: {black_wins} \ {num_episodes} \n White wins: {white_wins} \ {num_episodes}")
