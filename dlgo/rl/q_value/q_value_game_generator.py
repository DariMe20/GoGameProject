from keras import Sequential
from keras.src.saving.saving_api import load_model

from agent import QAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.rl.base_game_generator import GameGenerator

board_size = 9
encoder = SimpleEncoder((board_size, board_size))
model = Sequential()

path_Q1 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_models\\model_Q2.h5'
model_Q1 = load_model(path_Q1)
path_Q2 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\rl\\q_value\\q_models\\model_Q2_V2.h5'
model_Q2 = load_model(path_Q2)

agent1 = QAgent(model_Q1, encoder)
agent2 = QAgent(model_Q2, encoder)

output_folder = r'../../json_data/q_value/game_generator'
filename = r'../../json_data/q_value/game_generator/game_generator_summary.json'
experience_dir = r'../q_value/q_value_experience_files'

black_name = "model Q2"
white_name = "model Q2_v2"
temp_black = 0.02
temp_white = 0.02

q_game_generator = GameGenerator(agent_black=agent1, agent_white=agent2,
                                 black_key=black_name, white_key=white_name,
                                 temp_black=temp_black, temp_white=temp_white,
                                 output_folder=output_folder, filename=filename, experience_directory=experience_dir)

q_game_generator.generate_games(1, 9)
