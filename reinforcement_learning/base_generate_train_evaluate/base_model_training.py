import os

import h5py
import matplotlib
import matplotlib.pyplot as plt

from reinforcement_learning import load_experience
from utils import data_file_manipulator

# Set a non-interactive backend for Matplotlib
matplotlib.use('Agg')


class TrainingBase:
    @staticmethod
    def get_experience_files(experience_folder):
        experience_files = [os.path.join(experience_folder, f) for f in os.listdir(experience_folder) if
                            f.endswith('.h5')]
        return experience_files

    @staticmethod
    def train_agent(experience_folder, agent_in, agent_in_path, agent_out_path, lr, clip_norm, batch_size,
                    training_det):
        experience_files = TrainingBase.get_experience_files(experience_folder)
        experience_file_names = []
        all_history = []  # To collect all histories

        for exp_filename in experience_files:
            print('Training with %s...' % exp_filename)
            exp_buffer = load_experience(h5py.File(exp_filename, 'r'))
            history = agent_in.train(exp_buffer, lr=lr, clip_norm=clip_norm, batch_size=batch_size)

            experience_file_names.append(os.path.basename(exp_filename))
            all_history.append(history.history)  # Collect history

        # Salvează agentul actualizat
        with h5py.File(agent_out_path, 'w') as updated_agent_outf:
            agent_in.serialize(updated_agent_outf)

        TrainingBase.save_training_data_to_json(agent_in_path, agent_out_path, lr, clip_norm, batch_size,
                                                experience_file_names,
                                                training_det)

        # Plot loss
        TrainingBase.plot_training_loss(all_history)

    @staticmethod
    def plot_training_loss(all_history):
        loss = []
        val_loss = []
        for history in all_history:
            loss.extend(history['loss'])
            if 'val_loss' in history:
                val_loss.extend(history['val_loss'])

        epochs = range(1, len(loss) + 1)
        plt.plot(epochs, loss, 'bo', label='Training loss')

        plt.title('Training and validation loss')
        plt.legend()
        plt.savefig('training_validation_loss_GradientDescent.png')  # Save the plot as an image file

    @staticmethod
    def save_training_data_to_json(agent_in_path, agent_out_path, lr, clip_norm, batch_size, experience_files_names,
                                   training_details_filename):
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
