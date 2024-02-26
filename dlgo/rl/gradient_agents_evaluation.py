import os
import utils.constants
from dlgo import data_file_manipulator
from dlgo.goboard import GameState
from dlgo.gotypes import Player



# Inițializarea agenților
agent1_key = "Policy Gradient 5"
agent2_key = "Policy Gradient 4"
agent1 = utils.constants.BOTS[agent1_key]
agent2 = utils.constants.BOTS[agent2_key]

# INITIALIZARE DATE
black_wins = 0
white_wins = 0
total_black_score = 0
total_white_score = 0
board_size = 9
num_episodes = 1
game_results = []
output_folder = r'..\json_data'
filename = r'..\json_data\game_evaluation_summary.json'
os.makedirs(output_folder, exist_ok=True)


# METODA PENTRU GENERARE DE JOC
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
        'black_agent': agent1_key,
        'white_agent': agent2_key,
        'winner': state.winner(),
        'black_teritory': black_score,
        'white_teritory': white_score,
        'teritory_difference': difference
    }


# Parcurgere episoade
for episode in range(num_episodes):
    print(f"Started episode: {episode}")
    # Preluare informatii dupa joc
    game_info = play_game(agent1, agent2, board_size)
    if game_info['winner'] == Player.black:
        black_wins += 1
    else:
        white_wins += 1

    # Adaugare informatii la game_result
    score = {'black': black_wins, 'white': white_wins}
    game_results.append({
        'episode': episode,
        'winner': str(game_info['winner']),
        'current_score': score,
        'black_agent': str(game_info['black_agent']),
        'white_agent': str(game_info['white_agent'])
    })

    total_black_score += game_info['black_teritory']
    total_white_score += game_info['white_teritory']
    print(f"Finished episode {episode} with success!")


# GENERAREA DATELOR SI POPULAREA FISIERELOR JSON
average_black_score = total_black_score / num_episodes
average_white_score = total_white_score / num_episodes
print(f"Black wins: {black_wins} / {num_episodes} \nWhite wins: {white_wins} / {num_episodes}")

summary_info = {
    'Episodes': num_episodes,
    'Black_agent': agent1_key,
    'White_agent': agent2_key,
    'Black_wins': black_wins,
    'White_wins': white_wins,
    'Average_black_score': average_black_score,
    'Average_white_score': average_white_score
}

# SALVARE DATE IN FISIERE JSON
data_file_manipulator.generate_filename(agent1_key, agent2_key, output_folder)
data_file_manipulator.save_all_games_info(game_results, summary_info, agent1_key, agent2_key, output_folder)
data_file_manipulator.save_summary_info(summary_info, filename)