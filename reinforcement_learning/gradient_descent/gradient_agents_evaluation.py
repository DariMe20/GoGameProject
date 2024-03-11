import os

from keras.src.saving.saving_api import load_model

from agent import PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from reinforcement_learning.base_generate_train_evaluate.base_game_evaluator import GameEvaluator

# INITIALISE VARIABLES

board_size = 9
encoder = SimpleEncoder((board_size, board_size))

# MODEL PATHS
path_G1 = os.path.join('gradient_descent_models', 'model_Gradient1.h5')
path_G2 = os.path.join('gradient_descent_models', 'model_Gradient2.h5')

# LOAD MODELS
model_G1 = load_model(path_G1)
model_G2 = load_model(path_G2)

# CREATE AGENTS
agent1 = PolicyAgent(model_G1, encoder)
agent2 = PolicyAgent(model_G2, encoder)

# GET AGENT NAMES FROM MODEL FILES
black_name = os.path.splitext(os.path.basename(path_G1))[0]
white_name = os.path.splitext(os.path.basename(path_G2))[0]

# DATA SAVING PATHS
output_folder_outer = os.path.join('..', '..', 'dlgo', 'json_data', 'gradient_descent')
filename_outer = os.path.join('..', '..', 'dlgo', 'json_data', 'gradient_descent', 'game_evaluation_summary.json')


class GradientEvaluator(GameEvaluator):
    def __init__(self, agent_black=agent1, agent_white=agent2, black_key=black_name, white_key=white_name,
                 output_folder=output_folder_outer, filename=filename_outer):
        super().__init__(agent_black, agent_white, black_key, white_key, output_folder, filename)


# GIVE NUMBER OF SIMULATIONS AND RUN GENERATOR
NUM_EPISODES = 1
gradient_game_evaluator = GradientEvaluator()
gradient_game_evaluator.generate_games(NUM_EPISODES, encoder.board_width)
