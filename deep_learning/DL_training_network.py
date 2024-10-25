import os

from keras.src.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.src.saving.saving_api import load_model

from deep_learning.load_data_from_csv import load_data_from_csv, augment_data


def train_on_csv(csv_file, save_dir, model_dir, model_name):
    # Load and augment data
    X_train, X_val, Y_train, Y_val = load_data_from_csv(csv_file)
    X_train, Y_train = augment_data(X_train, Y_train)  # Augment only training data

    # Define callbacks
    es = EarlyStopping(monitor="val_accuracy", patience=10, restore_best_weights=True, verbose=1)
    rp = ReduceLROnPlateau(monitor="val_accuracy", factor=0.5, patience=5, min_lr=1e-5, verbose=1)

    model = load_model(f"{model_dir}/{model_name}.h5")
    # Train the model
    model.fit(X_train, Y_train,
              validation_data=(X_val, Y_val),
              epochs=100,
              batch_size=64,
              callbacks=[es, rp],
              verbose=1)

    # Save the model
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    model.save(os.path.join(save_dir, f"trained_{model_name}.h5"))
    print("Model saved successfully!")


# Training

train_on_csv(csv_file="data/go_training_data_test.csv",
             save_dir="trained_models/",
             model_name="TestNetwork",
             model_dir="models/")
