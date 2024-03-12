import os

from keras.src.saving.saving_api import load_model

from agent import QAgent
from dlgo.encoders.simple import SimpleEncoder
from reinforcement_learning.base_generate_train_evaluate.base_game_generator import GameGenerator

# INITIALISE VARIABLES

board_size = 9
encoder = SimpleEncoder((board_size, board_size))

# MODEL PATHS
path_Q1 = os.path.join('q_models', 'model_Q2.h5')
path_Q2 = os.path.join('q_models', 'model_Q2_V2.h5')

# DATA SAVING PATHS
output_folder_outer = os.path.join('..', '..', 'dlgo', 'json_data', 'q_value', 'game_generator')
filename_outer = os.path.join(output_folder_outer, 'game_generator_summary.json')
experience_dir_outer = os.path.join('q_value_experience_files')

# LOAD MODELS
model_Q1 = load_model(path_Q1)
model_Q2 = load_model(path_Q2)

# CREATE AGENTS
agent1 = QAgent(model_Q1, encoder)
agent2 = QAgent(model_Q2, encoder)

# GET AGENT NAMES FROM MODEL FILES
black_name = os.path.splitext(os.path.basename(path_Q1))[0]
white_name = os.path.splitext(os.path.basename(path_Q2))[0]

# SET AGENT EXPLORATION FACTOR
temp_black = 0.02
temp_white = 0.02


class QValueGameGenerator(GameGenerator):
    def __init__(self, agent_black=agent1, agent_white=agent2,
                 black_key=black_name, white_key=white_name,
                 black_temp=temp_black, white_temp=temp_white,
                 output_folder=output_folder_outer, filename=filename_outer, experience_directory=experience_dir_outer):
        super().__init__(agent_black, agent_white, black_key, white_key, black_temp, white_temp, output_folder,
                         filename, experience_directory)


# GIVE NUMBER OF SIMULATIONS AND RUN GENERATOR
NUM_EPISODES = 1
q_game_generator = QValueGameGenerator()
q_game_generator.generate_games(NUM_EPISODES, encoder.board_width)
