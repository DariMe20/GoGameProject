import os

import numpy as np
import pandas as pd
from sgfmill import sgf, boards


# Function to extract board states, next moves, and labels from an SGF file
def sgf_to_states_and_moves(sgf_file):
    with open(sgf_file, "rb") as f:
        sgf_game = sgf.Sgf_game.from_bytes(f.read())
        root_node = sgf_game.get_root()
        result = root_node.get("RE")
        moves = sgf_game.get_main_sequence()

    board_state = np.zeros((19, 19), dtype=int)
    board = boards.Board(19)
    state_move_pairs = []

    pass_count = 0

    for index, node in enumerate(moves):
        color, move = node.get_move()

        if move == (None, None) or move is None:
            if index == 0:
                continue

            state_move_pairs.append((board_state.copy(), "pass", 362))
            pass_count += 1
            if pass_count == 2:
                break
            continue

        pass_count = 0

        if color == 'b':
            label = move[0] * 19 + move[1] + 1
            board_state[move[0], move[1]] = 1
            board.play(move[0], move[1], 'b')
        elif color == 'w':
            label = move[0] * 19 + move[1] + 1
            board_state[move[0], move[1]] = -1
            board.play(move[0], move[1], 'w')

        state_move_pairs.append((board_state.copy(), (move[0], move[1]), label))

    if result and 'R' in result:
        state_move_pairs.append((board_state.copy(), "resign", 363))
        return state_move_pairs

    if result and ("+" in result) and pass_count < 2:
        state_move_pairs.append((board_state.copy(), "pass", 362))
        state_move_pairs.append((board_state.copy(), "pass", 362))

    return state_move_pairs


# Function to rotate board states and adjust moves for augmentation
def augment_data(state_move_pairs):
    augmented_data = []

    for board_state, move, label in state_move_pairs:
        for k in range(4):
            rotated_board = np.rot90(board_state, k)
            if isinstance(move, tuple):  # If it's a normal move
                x, y = move
                for _ in range(k):
                    x, y = 18 - y, x  # Rotate the coordinates
                new_move = f"{str(x).zfill(2)}{str(y).zfill(2)}"
            else:
                new_move = move  # For "pass" or "resign"

            augmented_data.append((rotated_board.tolist(), new_move, label))

    return augmented_data


# Function to write states, moves, and labels to a CSV file
def append_to_csv(csv_file, state_move_pairs):
    augmented_data = augment_data(state_move_pairs)

    if not os.path.isfile(csv_file):
        df = pd.DataFrame(columns=['Board State', 'Next Move', 'Label'])
        df.to_csv(csv_file, index=False)

    data = {
        'Board State': [pair[0] for pair in augmented_data],
        'Next Move': [pair[1] for pair in augmented_data],
        'Label': [pair[2] for pair in augmented_data]
        }

    df = pd.DataFrame(data)
    df.to_csv(csv_file, mode='a', header=False, index=False)
    print(f"Appended augmented data to CSV: {csv_file}")


# Function to check if an SGF file has been processed already
def is_processed(sgf_file, processed_file_list):
    with open(processed_file_list, 'r') as f:
        processed_files = f.read().splitlines()
    return sgf_file in processed_files


# Function to mark an SGF file as processed
def mark_as_processed(sgf_file, processed_file_list):
    with open(processed_file_list, 'a') as f:
        f.write(sgf_file + '\n')


# Main function
def main():
    sgf_directory = "data/test"
    csv_file = "data/go_training_data_test.csv"
    processed_file_list = "data/processed_sgf_files_test.txt"

    if not os.path.isfile(processed_file_list):
        open(processed_file_list, 'w').close()

    for sgf_file in os.listdir(sgf_directory):
        if sgf_file.endswith(".sgf"):
            sgf_path = os.path.join(sgf_directory, sgf_file)

            if not is_processed(sgf_file, processed_file_list):
                print(f"Processing file: {sgf_file}")
                state_move_pairs = sgf_to_states_and_moves(sgf_path)
                append_to_csv(csv_file, state_move_pairs)
                mark_as_processed(sgf_file, processed_file_list)
            else:
                print(f"File {sgf_file} has already been processed.")


if __name__ == "__main__":
    main()
