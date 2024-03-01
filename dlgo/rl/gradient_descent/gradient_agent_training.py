import os

import h5py
from keras.src.saving.saving_api import load_model

from dlgo import data_file_manipulator
from dlgo.agent import PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.rl import load_experience


def main():
    # Setează direct căile fișierelor și directoriilor
    board_size = 9
    encoder = SimpleEncoder((board_size, board_size))
    agent_in_path = '/dlgo/keras_networks/model_gradient4.h5'
    agent_out_path = '/dlgo/keras_networks/model_gradient5.h5'
    experience_folder = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\experience_files'
    training_details_filename = '../../json_data/training_data.json'

    # Inițializează o listă pentru a păstra numele fișierelor de experiență
    experience_files_names = []

    # Preia toate fișierele de experiență din director
    experience_files = [os.path.join(experience_folder, f) for f in os.listdir(experience_folder) if f.endswith('.h5')]

    # Încarcă agentul de învățare
    learning_model = load_model(agent_in_path)
    learning_agent = PolicyAgent(learning_model, encoder)

    lr = 0.0001
    clip_norm = 1.0
    batch_size = 712

    # Antrenează agentul folosind fiecare fișier de experiență
    for exp_filename in experience_files:
        print('Training with %s...' % exp_filename)
        exp_buffer = load_experience(h5py.File(exp_filename))
        learning_agent.train(exp_buffer, lr=lr, batch_size=batch_size)
        # Adaugă numele fișierului de experiență la listă
        experience_files_names.append(os.path.basename(exp_filename))

    # Salvează agentul actualizat
    with h5py.File(agent_out_path, 'w') as updated_agent_outf:
        learning_agent.serialize(updated_agent_outf)

    # Detalii despre antrenament pentru a fi salvate
    training_details = {
        'in_agent': os.path.basename(agent_in_path),
        'out_agent': os.path.basename(agent_out_path),
        'lr': lr,
        'clip_norm': clip_norm,
        'batch_size': batch_size,
        'experience_files': experience_files_names  # Adaugă lista de nume de fișiere de experiență
    }

    # Salvează detalii despre antrenament
    data_file_manipulator.save_training_details(training_details, training_details_filename)

if __name__ == '__main__':
    main()
