import os
from multiprocessing import Pool, cpu_count

import h5py

from dlgo.game_rules_implementation.Player import Player
from dlgo.game_rules_implementation.goboard import GameState
from reinforcement_learning import combine_experience
from reinforcement_learning.exerience_collector.experience_colector import ExperienceCollector
from utils import data_file_manipulator


def play_and_collect(board_size, agent_black, agent_white, black_key, white_key, temp_black, temp_white):
    game_state = GameState.new_game(board_size)
    collectors = [ExperienceCollector(), ExperienceCollector()]
    agents = {
        Player.black: agent_black,
        Player.white: agent_white,
    }
    agents[Player.black].set_collector(collectors[0])
    agents[Player.white].set_collector(collectors[1])
    agents[Player.black].collector.begin_episode()
    agents[Player.white].collector.begin_episode()

    while not game_state.is_over():
        next_player = game_state.next_player
        agent_next = agents[next_player]
        move = agent_next.select_move(game_state)
        game_state = game_state.apply_move(move)

    winner, scores = game_state.evaluate_territory()

    # Se finalizează colectarea experienței pentru ambii agenți
    if game_state.winner() == Player.black:
        agents[Player.black].collector.complete_episode(reward=1)
        agents[Player.white].collector.complete_episode(reward=-1)
    else:
        agents[Player.black].collector.complete_episode(reward=-1)
        agents[Player.white].collector.complete_episode(reward=1)

    return agents[Player.black].collector, agents[Player.white].collector


class GameGenerator:
    def __init__(self, agent_black, agent_white, black_key, white_key, temp_black, temp_white, output_folder,
                 filename, experience_directory):
        self.agent_black = agent_black
        self.agent_white = agent_white
        self.black_key = black_key
        self.white_key = white_key
        self.temp_black = temp_black
        self.temp_white = temp_white

        self.agent_black.set_temperature(self.temp_black)
        self.agent_white.set_temperature(self.temp_white)
        self.output_folder = output_folder
        self.filename = filename
        self.experience_directory = experience_directory

        self.game_results = []
        self.black_wins = 0
        self.white_wins = 0
        self.total_black_score = 0
        self.total_white_score = 0
        self.average_white_score = 0
        self.average_black_score = 0
        os.makedirs(output_folder, exist_ok=True)

        collector1 = ExperienceCollector()
        collector2 = ExperienceCollector()

        self.agent_black.set_collector(collector1)
        self.agent_white.set_collector(collector2)
        self.collectorB: ExperienceCollector = self.agent_black.collector
        self.collectorW: ExperienceCollector = self.agent_white.collector

    # METODA PENTRU JOC SI COLECTARE A EXPERIENTELOR
    def generate_games(self, num_episodes, board_size):
        pool_args = [(board_size, self.agent_black, self.agent_white, self.black_key, self.white_key, self.temp_black,
                      self.temp_white) for _ in range(num_episodes)]
        with Pool(cpu_count()) as pool:
            results = pool.starmap(play_and_collect, pool_args)

        # Combine experiences from all games
        combined_experience = combine_experience([item for sublist in results for item in sublist])

        # Save the combined experience
        self.save_experience(combined_experience)

    def save_experience(self, combined_experience):
        # Generate a unique filename for the experience data
        experience_filename = data_file_manipulator.generate_experience_filename(self.experience_directory)

        # Serialize a combined experience to an HDF5 file
        with h5py.File(experience_filename, 'w') as h5file:
            combined_experience.serialize(h5file)

    def reset_data(self):
        self.game_results = []
        self.black_wins = 0
        self.white_wins = 0
        self.total_black_score = 0
        self.total_white_score = 0
        self.average_white_score = 0
        self.average_black_score = 0
