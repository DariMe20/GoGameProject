import os

from keras.src.saving.saving_api import load_model

from agent import PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from reinforcement_learning.base_generate_train_evaluate.base_model_training import TrainingBase


def main():
    # Setează direct căile fișierelor și directoriilor
    board_size = 9
    encoder = SimpleEncoder((board_size, board_size))
    agent_in_path = os.path.join('gradient_descent_models', 'NO1_model_Gradient.h5')
    agent_out_path = os.path.join('gradient_descent_models', 'PlotTest_model_Gradient.h5')
    experience_folder = 'gradient_experience_files/Model1_Model1_6000games'
    training_details_filename = os.path.join('..', '..', 'dlgo', 'json_data', 'gradient_descent', 'training_data.json')

    # Încarcă agentul de învățare
    learning_model = load_model(agent_in_path)
    learning_agent = PolicyAgent(learning_model, encoder)

    # Setarea datelor de antrenament si antrenarea
    lr = 0.0008
    clip_norm = 1.0
    batch_size = 2048

    TrainingBase.train_agent(experience_folder, learning_agent, agent_in_path, agent_out_path,
                             lr, clip_norm, batch_size, training_details_filename)
    learning_agent.model.summary()


if __name__ == '__main__':
    main()
