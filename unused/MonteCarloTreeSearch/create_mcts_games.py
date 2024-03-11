import argparse

import numpy as np

from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.game_rules_implementation.goboard import GameState
from unused.MonteCarloTreeSearch import MCTS
from utils.utils import print_board, print_move


def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []
    board_size = (board_size, board_size)
    encoder = OnePlaneEncoder(board_size)

    game = GameState.new_game(board_size)
    bot = MCTS.MCTSAgent(rounds, temperature)
    num_moves = 0

    while not game.is_over():
        # Funcția print_board ar trebui să afișeze tabla de joc în consolă.
        print_board(game.board)

        # Agentul MCTS selectează următoarea mutare
        move = bot.select_moveMCTS(game)

        if move.is_play:
            # Codifică starea jocului curent și o adaugă la lista de table de joc
            boards.append(encoder.encode(game))

            # Inițializează un vector one-hot pentru reprezentarea mutării
            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            moves.append(move_one_hot)

            # Funcția print_move ar trebui să afișeze mutarea efectuată în consolă.
            print_move(game.next_player, move)

        # Aplică mutarea la starea jocului
        game = game.apply_move(move)
        num_moves += 1

        if num_moves > max_moves:
            break

    return np.array(boards), np.array(moves)


# Presupunând că funcția generate_game este definită, așa cum am discutat anterior.

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', '-b', type=int, default=9)
    parser.add_argument('--rounds', '-r', type=int, default=5)
    parser.add_argument('--temperature', '-t', type=float, default=0.8)
    parser.add_argument('--max-moves', '-m', type=int, default=60, help='Max moves per game.')
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--board-out')
    parser.add_argument('--move-out')
    args = parser.parse_args()

    xs = []
    ys = []

    for i in range(args.num_games):
        print('Generating game %d/%d...' % (i + 1, args.num_games))
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)
        xs.append(x)
        ys.append(y)

    x = np.concatenate(xs)
    y = np.concatenate(ys)

    # Salvarea stărilor jocului și a mutărilor în fișiere .npy specificate.
    np.save(args.board_out, x)
    np.save(args.move_out, y)


if __name__ == '__main__':
    main()
