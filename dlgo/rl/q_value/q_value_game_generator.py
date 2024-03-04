import os

import h5py
from keras import Sequential
from keras.src.saving.saving_api import load_model

from utils import data_file_manipulator
from dlgo.agent import QAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.game_rules_implementation.goboard import GameState
from dlgo.game_rules_implementation.gotypes import Player
from dlgo.rl import experience
from dlgo.rl.experience_colector import ExperienceCollector

board_size = 9
encoder = SimpleEncoder((board_size, board_size))
model = Sequential()

path_Q1 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_models\\model_Q2.h5'
model_Q1 = load_model(path_Q1)
path_Q2 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_models\\model_Q2_V2.h5'
model_Q2 = load_model(path_Q2)

agent1 = QAgent(model_Q1, encoder)
agent2 = QAgent(model_Q2, encoder)

collector1 = ExperienceCollector()
collector2 = ExperienceCollector()

agent1.set_collector(collector1)
agent2.set_collector(collector2)

# STABILIRE CULORI AGENTI
black_agent = agent1
white_agent = agent2
black_key = "Q agent 2 V2"
white_key = "Q agent 2"

# SETARE NIVEL DE EXPLORARE PE AGENTI
black_agent.set_temperature(0.02)
white_agent.set_temperature(0.02)

# INITIALIZARE DATE
num_episodes = 100
black_wins = 0
white_wins = 0
total_black_score = 0
total_white_score = 0
black_temperature = black_agent.temperature if black_agent.temperature else 0.0
white_temperature = white_agent.temperature if white_agent.temperature else 0.0

game_results = []
output_folder = r'../../json_data/q_value/game_generator'
filename = r'../../json_data/q_value/game_generator/game_generator_summary.json'
experience_directory = r'../q_value/q_value_experience_files'
os.makedirs(output_folder, exist_ok=True)


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

    winner, scores = state.evaluate_territory()
    black_score = scores[Player.black]
    white_score = scores[Player.white]

    difference = abs(black_score - white_score)

    # Returnare date folosite in json
    return {
        'black_agent': black_key,
        'white_agent': white_key,
        'winner': state.winner(),
        'black_territory': black_score,
        'white_territory': white_score,
        'territory_difference': difference,
        'black_temperature': black_temperature,
        'white_temperature': white_temperature
        }


for episode in range(num_episodes):
    print("Started episode: ", episode)
    collector1.begin_episode()
    collector2.begin_episode()

    # Preluare informatii dupa joc
    game_info = play_game(agent1, agent2, board_size)
    if game_info['winner'] == Player.black:
        black_wins += 1
        collector1.complete_episode(reward=1)
        collector2.complete_episode(reward=-1)
    else:
        collector2.complete_episode(reward=1)
        collector1.complete_episode(reward=-1)
        white_wins += 1

    # Adaugare informatii la game_result
    score = {'black': black_wins, 'white': white_wins}
    game_results.append({
        'episode': episode,
        'winner': str(game_info['winner']),
        'current_score': score,
        'black_agent': str(game_info['black_agent']),
        'white_agent': str(game_info['white_agent']),
        'black_score': str(game_info['black_territory']),
        'white_score': str(game_info['white_territory']),
        'territory_difference': str(game_info['territory_difference']),
        'black_temperature': str(game_info['black_temperature']),
        'white_temperature': str(game_info['white_temperature'])
        })

    total_black_score += game_info['black_territory']
    total_white_score += game_info['white_territory']
    print(f"Finished episode {episode} with success!")


experience_combined = experience.combine_experience([collector1, collector2])
experience_filename = data_file_manipulator.generate_experience_filename(experience_directory)
with h5py.File(experience_filename, 'w') as experience_outf:
    experience_combined.serialize(experience_outf)

# GENERAREA DATELOR SI POPULAREA FISIERELOR JSON
average_black_score = total_black_score / num_episodes
average_white_score = total_white_score / num_episodes
print(f"Black wins: {black_wins} / {num_episodes} \nWhite wins: {white_wins} / {num_episodes}")

summary_info = {
    'Episodes': num_episodes,
    'Black_agent': black_key,
    'White_agent': white_key,
    'Black_wins': black_wins,
    'White_wins': white_wins,
    'Average_black_score': average_black_score,
    'Average_white_score': average_white_score,
    'black_temperature (epsilon)': black_temperature,
    'white_temperature (epsilon)': white_temperature
}

# SALVARE DATE IN FISIERE JSON
data_file_manipulator.generate_filename(black_key, white_key, output_folder)
data_file_manipulator.save_all_games_info(game_results, summary_info, black_key, white_key, output_folder)
data_file_manipulator.save_summary_info(summary_info, filename)