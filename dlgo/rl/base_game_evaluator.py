import os

from dlgo.game_rules_implementation.Player import Player
from dlgo.game_rules_implementation.goboard import GameState
from utils import data_file_manipulator


class GameEvaluator:
    def __init__(self, agent_black, agent_white, black_key, white_key, output_folder, filename):

        self.agent_black = agent_black
        self.agent_white = agent_white
        self.black_key = black_key
        self.white_key = white_key

        self.output_folder = output_folder
        self.filename = filename

        self.game_results = []
        self.black_wins = 0
        self.white_wins = 0
        self.total_black_score = 0
        self.total_white_score = 0
        self.average_white_score = 0
        self.average_black_score = 0
        os.makedirs(output_folder, exist_ok=True)

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
            }

    def generate_games(self, num_episodes, board_size):
        for episode in range(num_episodes):
            print("Started episode: ", episode)

            # Preluare informatii dupa joc
            game_info = self.play_game(board_size)
            if game_info['winner'] == Player.black:
                self.black_wins += 1
            else:
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
                'territory_difference': str(game_info['territory_difference'])
                })

            self.total_black_score += game_info['black_territory']
            self.total_white_score += game_info['white_territory']
            print(f"Finished episode {episode} with success!")

        # GENERAREA DATELOR SI POPULAREA FISIERELOR JSON
        self.average_black_score = self.total_black_score / num_episodes
        self.average_white_score = self.total_white_score / num_episodes
        print(f"Black wins: {self.black_wins} / {num_episodes} \nWhite wins: {self.white_wins} / {num_episodes}")
        self.save_summary_info(num_episodes)
        self.reset_data()

    def save_summary_info(self, num_episodes):
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
