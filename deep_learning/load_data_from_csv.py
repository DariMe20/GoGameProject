import random

import numpy as np
import pandas as pd
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split


# 1. Load data from CSV
def load_data_from_csv(csv_file):
    data = pd.read_csv(csv_file)

    # Extract board states and moves
    board_states = data['Board State'].apply(eval).values
    labels = data['Label'].values  # Load labels for each move

    # Convert board states to numpy array and reshape them for CNN
    X = np.array([np.array(board).reshape(19, 19) for board in board_states])
    X = X.reshape(-1, 19, 19, 1)  # Add a channel dimension for CNN input

    # Convert labels to categorical (19*19 + 2 classes for pass/resign)
    Y = to_categorical(labels - 1, num_classes=363)  # Adjust labels to range 0-362 for to_categorical

    # Split data into training and validation sets
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=42)

    return X_train, X_val, Y_train, Y_val


# 2. Data Augmentation by rotating the board
def augment_data(X, Y):
    augmented_X, augmented_Y = [], []
    for i in range(len(X)):
        for _ in range(4):  # Rotate 4 times (0°, 90°, 180°, 270°)
            augmented_X.append(np.rot90(X[i], k=random.randint(0, 3)))  # Random rotation
            augmented_Y.append(Y[i])
    return np.array(augmented_X), np.array(augmented_Y)
