
from keras.src.saving.saving_api import load_model
from keras.models import Sequential

import utils.constants
from dlgo.agent.policy_agent import PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.goboard import GameState
from dlgo.gotypes import Player

board_size = 9

agent1 = utils.constants.BOTS["Policy Gradient 3"]
agent2 = utils.constants.BOTS["Policy Gradient 5"]

black_wins = 0
white_wins = 0


# METODA PENTRU JOC SI COLECTARE A EXPERIENTELOR
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
    return state.winner()



# SETAREA NUMARULUI DE EPISOADE SI APELAREA METODELOR DE ANTRENARE
num_episodes = 10

for episode in range(num_episodes):
    print("Started episode: ", episode)

    game_record = play_game(agent1, agent2, board_size)
    if game_record == Player.black:
        black_wins += 1
    else:
        white_wins += 1
    print(f"Finished episode {episode} with success!")


print(f"Black wins: {black_wins} \ {num_episodes} \n White wins: {white_wins} \ {num_episodes}")
