import os
import random

import numpy as np
import pandas as pd
from keras import Sequential
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
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


# 3. CNN Model definition
def create_model():
    model = Sequential()
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(19, 19, 1)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))

    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(19 * 19 + 2, activation='softmax'))  # 19x19 moves + pass + resign

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# 4. Main function for training with CSVs and augmented data
def train_on_csv(csv_file):
    # Load and augment data
    X_train, X_val, Y_train, Y_val = load_data_from_csv(csv_file)
    X_train, Y_train = augment_data(X_train, Y_train)  # Augment only training data

    # Create and compile model
    model = create_model()

    # Define callbacks
    es = EarlyStopping(monitor="val_accuracy", patience=10, restore_best_weights=True, verbose=1)
    rp = ReduceLROnPlateau(monitor="val_accuracy", factor=0.5, patience=5, min_lr=1e-5, verbose=1)

    # Train the model
    model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=100, batch_size=64, callbacks=[es, rp],
              verbose=1)

    # Save the model
    model_dir = 'models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model.save(os.path.join(model_dir, 'model_19x19_augmented.h5'))
    print("Model saved successfully!")


# Training
csv_file = "data/go_training_data_test.csv"
train_on_csv(csv_file)
