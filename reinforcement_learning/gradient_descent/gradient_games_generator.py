import os

from keras.src.saving.saving_api import load_model

from agent import PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from reinforcement_learning.base_generate_train_evaluate.base_game_generator import GameGenerator

# INITIALISE VARIABLES

board_size = 9
encoder = SimpleEncoder((board_size, board_size))

# MODEL PATHS
path_G1 = os.path.join('gradient_descent_models', 'model_gradient1.h5')
path_G2 = os.path.join('gradient_descent_models', 'model_gradient2.h5')

# LOAD MODELS
model_G1 = load_model(path_G1)
model_G2 = load_model(path_G2)

# CREATE AGENTS
agent1 = PolicyAgent(model_G1, encoder)
agent2 = PolicyAgent(model_G2, encoder)

# GET AGENT NAMES FROM MODEL FILES
black_name = os.path.splitext(os.path.basename(path_G1))[0]
white_name = os.path.splitext(os.path.basename(path_G2))[0]

# SET AGENT EXPLORATION FACTOR
temp_black = 0.02
temp_white = 0.02

# DATA SAVING PATHS
output_folder_outer = os.path.join('..', '..', 'dlgo', 'json_data', 'gradient_descent', 'game_generator')
filename_outer = os.path.join(output_folder_outer, 'game_generator_summary.json')
experience_dir_outer = os.path.join('gradient_experience_files')


class GradientGameGenerator(GameGenerator):
    def __init__(self, agent_black=agent1, agent_white=agent2,
                 black_key=black_name, white_key=white_name,
                 black_temp=temp_black, white_temp=temp_white,
                 output_folder=output_folder_outer, filename=filename_outer, experience_directory=experience_dir_outer):
        super().__init__(agent_black, agent_white, black_key, white_key, black_temp, white_temp, output_folder,
                         filename, experience_directory)


# GIVE NUMBER OF SIMULATIONS AND RUN GENERATOR
NUM_EPISODES = 1
gradient_game_generator = GradientGameGenerator()
gradient_game_generator.generate_games(NUM_EPISODES, encoder.board_width)
