import os

from keras.src.saving.saving_api import load_model

from agent import QAgent
from dlgo.encoders.simple import SimpleEncoder
from reinforcement_learning.base_generate_train_evaluate.base_game_evaluator import GameEvaluator

# INITIALISE VARIABLES

board_size = 9
encoder = SimpleEncoder((board_size, board_size))

# MODEL PATHS
path_Q1 = os.path.join('q_models', 'model_Q2.h5')
path_Q2 = os.path.join('q_models', 'model_Q2_V2.h5')

# LOAD MODELS
model_Q1 = load_model(path_Q1)
model_Q2 = load_model(path_Q2)

# CREATE AGENTS
agent1 = QAgent(model_Q1, encoder)
agent2 = QAgent(model_Q2, encoder)

# GET AGENT NAMES FROM MODEL FILES
black_name = os.path.splitext(os.path.basename(path_Q1))[0]
white_name = os.path.splitext(os.path.basename(path_Q2))[0]

# DATA SAVING PATHS
output_folder_outer = os.path.join('..', '..', 'dlgo', 'json_data', 'q_value', 'game_evaluation')
filename_outer = os.path.join(output_folder_outer, 'evaluation_summary.json')


class QValueEvaluator(GameEvaluator):
    def __init__(self, agent_black=agent1, agent_white=agent2, black_key=black_name, white_key=white_name,
                 output_folder=output_folder_outer, filename=filename_outer):
        super().__init__(agent_black, agent_white, black_key, white_key, output_folder, filename)


# GIVE NUMBER OF SIMULATIONS AND RUN GENERATOR
NUM_EPISODES = 1
q_game_evaluator = QValueEvaluator()
q_game_evaluator.generate_games(NUM_EPISODES, encoder.board_width)