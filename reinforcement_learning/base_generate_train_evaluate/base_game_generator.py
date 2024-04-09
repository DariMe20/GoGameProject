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
    black_score = scores[Player.black]
    white_score = scores[Player.white]
    difference = abs(black_score - white_score)

    # Se finalizează colectarea experienței pentru ambii agenți
    if game_state.winner() == Player.black:
        agents[Player.black].collector.complete_episode(reward=1)
        agents[Player.white].collector.complete_episode(reward=-1)
    else:
        agents[Player.black].collector.complete_episode(reward=-1)
        agents[Player.white].collector.complete_episode(reward=1)

    game_result = {
        'black_agent': black_key,
        'white_agent': white_key,
        'winner': game_state.winner(),
        'black_territory': black_score,
        'white_territory': white_score,
        'territory_difference': difference,
        }

    return [agents[Player.black].collector, agents[Player.white].collector], game_result


class GameGenerator:
    def __init__(self, agent_black, agent_white, black_key, white_key, temp_black, temp_white, output_folder,
                 filename, experience_directory):
        self.all_episodes_info = []
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

        # Inițializează o listă pentru a colecta toate experiențele
        all_collectors_experience = []

        # Procesează fiecare rezultat returnat
        for collectors, game_info in results:
            all_collectors_experience.extend(collectors)  # Adaugă colectoarele de experiență pentru combinare

            if game_info['winner'] == Player.black:
                self.black_wins += 1
            else:
                self.white_wins += 1
            current_score = 0 if game_info['winner'] == Player.black else 1
            # Adaugare informatii la game_result
            self.game_results.append({
                'winner': str(game_info['winner']),
                'current_score': str(current_score),
                'black_agent': str(game_info['black_agent']),
                'white_agent': str(game_info['white_agent']),
                'black_score': str(game_info['black_territory']),
                'white_score': str(game_info['white_territory']),
                'territory_difference': str(game_info['territory_difference'])
                })

            self.total_black_score += game_info['black_territory']
            self.total_white_score += game_info['white_territory']

        # Combinează experiențele din toate jocurile
        combined_experience = combine_experience(all_collectors_experience)

        # Salvează experiența combinată
        # self.save_experience(combined_experience)

        # GENERAREA DATELOR SI POPULAREA FISIERELOR JSON
        self.average_black_score = self.total_black_score / num_episodes
        self.average_white_score = self.total_white_score / num_episodes
        print(f"Black wins: {self.black_wins} / {num_episodes} \nWhite wins: {self.white_wins} / {num_episodes}")
        self.save_summary_info(num_episodes, combined_experience)
        self.reset_data()

    def save_experience(self, combined_experience):
        # Generate a unique filename for the experience data
        experience_filename = data_file_manipulator.generate_experience_filename(self.experience_directory,
                                                                                 self.black_key, self.white_key)

        # Serialize a combined experience to an HDF5 file
        with h5py.File(experience_filename, 'w') as h5file:
            combined_experience.serialize(h5file)

    def save_summary_info(self, num_episodes, combined_experience):
        # Generate a unique filename for the experience data
        experience_filename = data_file_manipulator.generate_experience_filename(self.experience_directory,
                                                                                 self.black_key, self.white_key)

        # Serialize a combined experience to an HDF5 file
        with h5py.File(experience_filename, 'w') as h5file:
            combined_experience.serialize(h5file)

        summary_info = {
            'Episodes': num_episodes,
            'Black_agent': self.black_key,
            'White_agent': self.white_key,
            'Black_wins': self.black_wins,
            'White_wins': self.white_wins,
            'Average_black_score': self.average_black_score,
            'Average_white_score': self.average_white_score,
            }

        # SALVARE DATE IN FISIERE JSON
        data_file_manipulator.generate_filename(self.black_key, self.white_key, self.output_folder, num_episodes)
        data_file_manipulator.save_all_games_info(self.game_results,
                                                  summary_info,
                                                  self.black_key, self.white_key,
                                                  self.output_folder, num_episodes)
        data_file_manipulator.save_summary_info(summary_info, self.filename, experience_filename)

        data_file_manipulator.save_all_episodes_info(self.game_results, self.output_folder)

    def reset_data(self):
        self.game_results = []
        self.black_wins = 0
        self.white_wins = 0
        self.total_black_score = 0
        self.total_white_score = 0
        self.average_white_score = 0
        self.average_black_score = 0
