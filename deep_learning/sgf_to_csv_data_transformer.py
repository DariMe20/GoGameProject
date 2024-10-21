import os

import numpy as np
import pandas as pd
from sgfmill import sgf, boards


# Function to extract board states and moves from an SGF file
def sgf_to_states_and_moves(sgf_file):
    with open(sgf_file, "rb") as f:
        sgf_game = sgf.Sgf_game.from_bytes(f.read())
        moves = sgf_game.get_main_sequence()

    # Initial state of the board (19x19 Go board)
    board_state = np.zeros((19, 19), dtype=int)
    board = boards.Board(19)  # Create a board of size 19x19
    state_move_pairs = []

    # Loop through all the moves
    for node in moves:
        color, move = node.get_move()
        if move is None:  # Skip if it's not a move node (comments, etc.)
            continue

        x, y = move
        if color == 'b':  # Black is represented by 1
            board.play(x, y, 'b')  # Update the internal board state
            board_state[x, y] = 1  # Update our matrix representation
        elif color == 'w':  # White is represented by -1
            board.play(x, y, 'w')  # Update the internal board state
            board_state[x, y] = -1  # Update our matrix representation

        # Append the current board state and move
        state_move_pairs.append((board_state.copy(), (x, y)))

    return state_move_pairs


# Function to write states and moves to a CSV file
def append_to_csv(csv_file, state_move_pairs):
    # Check if the CSV file exists already
    if not os.path.isfile(csv_file):
        print(f"Creating new CSV file: {csv_file}")
        df = pd.DataFrame(columns=['Board State', 'Next Move'])
        df.to_csv(csv_file, index=False)

    # Prepare data for appending to CSV
    data = {
        'Board State': [pair[0].tolist() for pair in state_move_pairs],  # The board state matrix
        'Next Move': [f"{pair[1][0]}{pair[1][1]}" for pair in state_move_pairs]  # The move coordinates
        }

    df = pd.DataFrame(data)
    df.to_csv(csv_file, mode='a', header=False, index=False)
    print(f"Appended data to CSV: {csv_file}")


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
    # Assuming you are already in the 'deep_learning' directory
    sgf_directory = "data/sgf"
    csv_file = "go_training_data.csv"
    processed_file_list = "processed_sgf_files.txt"

    # Check if the processed file list exists, create if not
    if not os.path.isfile(processed_file_list):
        print(f"Creating processed file list: {processed_file_list}")
        open(processed_file_list, 'w').close()

    # Loop through all SGF files in the specified directory
    for sgf_file in os.listdir(sgf_directory):
        if sgf_file.endswith(".sgf"):  # Only process SGF files
            sgf_path = os.path.join(sgf_directory, sgf_file)

            # Check if the SGF file has been processed before
            if not is_processed(sgf_file, processed_file_list):
                print(f"Processing file: {sgf_file}")

                # Extract board states and moves
                state_move_pairs = sgf_to_states_and_moves(sgf_path)

                # Append the data to the CSV file
                append_to_csv(csv_file, state_move_pairs)

                # Mark the SGF file as processed
                mark_as_processed(sgf_file, processed_file_list)
            else:
                print(f"File {sgf_file} has already been processed.")


if __name__ == "__main__":
    main()
