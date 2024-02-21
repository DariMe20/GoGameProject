import os
import h5py
from keras import Sequential
from keras.src.saving.saving_api import load_model

from dlgo.agent import load_policy_agent, PolicyAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.rl import load_experience

def main():
    # Setează direct căile fișierelor și directoriilor
    board_size = 9
    encoder = SimpleEncoder((board_size, board_size))
    agent_in_path = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient3.h5'
    agent_out_path = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient4.h5'
    experience_folder = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\experience_files'

    # Preia toate fișierele de experiență din director
    experience_files = [os.path.join(experience_folder, f) for f in os.listdir(experience_folder) if f.endswith('.h5')]

    # Încarcă agentul de învățare
    learning_model = load_model(agent_in_path)
    learning_agent = PolicyAgent(learning_model, encoder)



    # Antrenează agentul folosind fiecare fișier de experiență
    for exp_filename in experience_files:
        print('Training with %s...' % exp_filename)
        exp_buffer = load_experience(h5py.File(exp_filename, 'r'))
        learning_agent.train(exp_buffer)

    # Salvează agentul actualizat
    with h5py.File(agent_out_path, 'w') as updated_agent_outf:
        learning_agent.serialize(updated_agent_outf)

if __name__ == '__main__':
    main()
