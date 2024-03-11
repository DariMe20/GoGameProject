import os

import h5py

from dlgo.game_rules_implementation.Player import Player
from dlgo.game_rules_implementation.goboard import GameState
from reinforcement_learning.exerience_collector import experience
from reinforcement_learning.exerience_collector.experience_colector import ExperienceCollector
from utils import data_file_manipulator


class GameGenerator:
    def __init__(self, agent_black, agent_white, black_key, white_key, temp_black, temp_white, output_folder,
                 filename, experience_directory):

        self.agent_black = agent_black
        self.agent_white = agent_white
        self.black_key = black_key
        self.white_key = white_key
        self.temp_black = temp_black
        self.temp_white = temp_white

        if self.agent_white.temperature and self.agent_black.temperature:
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
    def play_game(self, board_size):
        state = GameState.new_game(board_size)
        agents = {
            Player.black: self.agent_black,
            Player.white: self.agent_white
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
            'black_agent': self.black_key,
            'white_agent': self.white_key,
            'winner': state.winner(),
            'black_territory': black_score,
            'white_territory': white_score,
            'territory_difference': difference,
            'black_temperature': self.temp_black,
            'white_temperature': self.temp_white
            }

    def generate_games(self, num_episodes, board_size):
        for episode in range(num_episodes):
            print("Started episode: ", episode)
            self.agent_black.collector.begin_episode()
            self.agent_white.collector.begin_episode()

            # Preluare informatii dupa joc
            game_info = self.play_game(board_size)
            if game_info['winner'] == Player.black:
                self.black_wins += 1
                self.collectorB.complete_episode(reward=1)
                self.collectorW.complete_episode(reward=-1)
            else:
                self.collectorB.complete_episode(reward=1)
                self.collectorW.complete_episode(reward=-1)
                self.white_wins += 1

            # Adaugare informatii la game_result
            score = {'black': self.black_wins, 'white': self.white_wins}
            self.game_results.append({
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

            self.total_black_score += game_info['black_territory']
            self.total_white_score += game_info['white_territory']
            print(f"Finished episode {episode} with success!")

        # GENERAREA DATELOR SI POPULAREA FISIERELOR JSON
        self.average_black_score = self.total_black_score / num_episodes
        self.average_white_score = self.total_white_score / num_episodes
        print(f"Black wins: {self.black_wins} / {num_episodes} \nWhite wins: {self.white_wins} / {num_episodes}")
        self.save_experience(num_episodes)
        self.reset_data()

    def save_experience(self, num_episodes):
        summary_info = {
            'Episodes': num_episodes,
            'Black_agent': self.black_key,
            'White_agent': self.white_key,
            'Black_wins': self.black_wins,
            'White_wins': self.white_wins,
            'Average_black_score': self.average_black_score,
            'Average_white_score': self.average_white_score,
            'black_temperature (epsilon)': self.temp_black,
            'white_temperature (epsilon)': self.temp_white
            }

        experience_combined = experience.combine_experience([self.agent_black.collector, self.agent_white.collector])
        experience_filename = data_file_manipulator.generate_experience_filename(self.experience_directory)
        with h5py.File(experience_filename, 'w') as experience_outf:
            experience_combined.serialize(experience_outf)

        # SALVARE DATE IN FISIERE JSON
        data_file_manipulator.generate_filename(self.black_key, self.white_key, self.output_folder)
        data_file_manipulator.save_all_games_info(self.game_results,
                                                  summary_info,
                                                  self.black_key, self.white_key,
                                                  self.output_folder)
        data_file_manipulator.save_summary_info(summary_info, self.filename)

    def reset_data(self):
        self.game_results = []
        self.black_wins = 0
        self.white_wins = 0
        self.total_black_score = 0
        self.total_white_score = 0
        self.average_white_score = 0
        self.average_black_score = 0
