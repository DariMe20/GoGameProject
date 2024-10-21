import os

import keras
import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.src.layers import Dropout, BatchNormalization
from keras.utils import to_categorical


# 1. Load data from CSV
def load_data_from_csv(csv_file):
    data = pd.read_csv(csv_file)

    # Extract board states and moves
    board_states = data['Board State'].apply(eval).values
    moves = data['Next Move'].values

    # Convert board states to numpy array and reshape them for CNN
    X = np.array([np.array(board).reshape(19, 19) for board in board_states])
    X = X.reshape(-1, 19, 19, 1)  # Add a channel dimension for CNN input

    # Convert move strings (2, 3, or 4 characters) to (x, y) coordinates
    Y = []
    for move in moves:
        if isinstance(move, str):
            if move == "pass":
                Y.append(361)  # Special index for "pass"
            elif move == "resign":
                Y.append(362)  # Special index for "resign"
            else:
                try:
                    if len(move) == 2:  # ex: "55"
                        x = int(move[0])
                        y = int(move[1])
                    elif len(move) == 3:  # ex: "115" or "158"
                        x = int(move[0])
                        y = int(move[1:])
                    elif len(move) == 4:  # ex: "1115"
                        x = int(move[:2])
                        y = int(move[2:])
                    else:
                        print(f"Skipping invalid move: {move}")
                        continue
                    # Transform the move into a single index for the 19x19 board
                    Y.append(x * 19 + y)
                except ValueError:
                    print(f"Invalid move format: {move}")
                    continue
        else:
            print(f"Skipping non-int move: {move}")

    Y = np.array(Y)

    # Convert moves to categorical for softmax, with 19*19 + 2 classes (for "pass" and "resign")
    Y = to_categorical(Y, num_classes=19 * 19 + 2)  # 363 possible classes
    return X, Y


# 2. Load the data
csv_file = "data/go_training_data.csv"
X, Y = load_data_from_csv(csv_file)

# 3. Split the data into training and test sets
np.random.seed(123)
samples = X.shape[0]
train_samples = int(0.9 * samples)
X_train, X_test = X[:train_samples], X[train_samples:]
Y_train, Y_test = Y[:train_samples], Y[train_samples:]

# Define the CNN model
model = Sequential()

# Simplified convolutional layers with max pooling
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(19, 19, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())

model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())

model.add(Flatten())

# Simplified dense layers
model.add(Dense(256, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(19 * 19 + 2, activation='softmax'))  # 19*19 possible moves + 1 for pass + 1 for resign

# Compile the model
model.compile(optimizer='SGD', loss="categorical_crossentropy", metrics=['accuracy'])

es = keras.callbacks.EarlyStopping(
    monitor="val_accuracy",  # metrics to monitor
    patience=10,  # how many epochs before stop
    verbose=1,  # make it talk
    mode="max",  # we need the maximum accuracy.
    restore_best_weights=True,  # after training, model automatically restores best metrics
    )

# rp = ReduceLROnPlateau Callback
rp = keras.callbacks.ReduceLROnPlateau(
    monitor="val_accuracy",  # analyse validation accuracy
    factor=0.2,  # reduce lr with 20% when validation accuracy performance decreases
    patience=3,  # over 3 consecutive epochs
    verbose=1,
    mode="max",  # we need the best value
    min_lr=0.00001,  # minimum lr - it cannot decrease anymore than this value
    )

# Antrenează modelul folosind ponderi pentru clase
model.fit(X_train, Y_train,
          batch_size=32,
          epochs=100,
          verbose=1,
          validation_data=(X_test, Y_test),
          callbacks=[es, rp])

# 7. Evaluate the model
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# 8. Save the model
model_dir = 'models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

model_path = os.path.join(model_dir, 'model_test.h5')
model.save(model_path)
print("Modelul a fost salvat cu succes")
