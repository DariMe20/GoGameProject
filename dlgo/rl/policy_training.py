import keras
import numpy as np
import tensorflow as tf

from keras.src.regularizers import l2
from keras.src.saving.saving_api import load_model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import Adam
from dlgo.agent.policy_agent import PolicyAgent
from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.simple import SimpleEncoder
from dlgo.goboard import GameState
from dlgo.gotypes import Player
from dlgo.keras_networks import large_network
from dlgo.rl.experience_colector import ExperienceCollector


board_size = 9
encoder = SimpleEncoder((board_size, board_size))
model = Sequential()

# Adaugare layere neuronale in model pentru ambii agenti
model_policy = Sequential()
for layer in large_network.layers(encoder.shape()):
    model_policy.add(layer)
model_policy.add(Dense(encoder.num_points(), kernel_regularizer=l2(0.001)))
model_policy.add(Dropout(0.3))
model_policy.add(Activation('softmax'))

model_path_predict = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model2.h5'
model_path_policy = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\black_agent_model3.h5'
model_predict = load_model(model_path_predict)
# model_policy = load_model(model_path_policy)

# Initializare agenti pe 2 culori si colectori de experienta
agent_black = PolicyAgent(model_policy, encoder, color=Player.black)
agent_white = DeepLearningAgent(model_predict, encoder)

collector_black = ExperienceCollector()
agent_black.set_collector(collector_black)

#INITIALIZARE OPTIMIZATORI
optimizer_black = Adam(learning_rate=0.001)
model_policy.compile(optimizer=optimizer_black, loss='sparse_categorical_crossentropy')
optimizer_black.build(model_policy.trainable_variables)


# METODA PENTRU JOC SI COLECTARE A EXPERIENTELOR
def play_game(agent_black, agent_white, board_size):
    state = GameState.new_game(board_size)
    agents = {Player.black: agent_black, Player.white: agent_white}
    last_num_prisoners = 0

    while not state.is_over():
        next_player = state.next_player
        agent_next = agents[next_player]
        if agent_next == Player.white:
            move = agent_next.select_move(state)
            state = state.apply_move(move)
        else:
            move = agent_next.select_move(state)

            if state.is_move_atari(move):
                collector_black.complete_episode(0.5)
            elif state.is_move_protect(move):
                collector_black.complete_episode(0.5)
            elif state.is_move_capture(move):
                collector_black.complete_episode(1)
            else:
                collector_black.complete_episode(-0.5)

            state = state.apply_move(move)

    winner, score = state.winner()
    if winner is not None:
        if winner == Player.black:
            collector_black.complete_episode(7)
        else:
            if score < 20:
                collector_black.complete_episode(-1.75)
            else:
                collector_black.complete_episode(-3.5)
    else:
        collector_black.complete_episode(0)



# METODA PENTRU ANTRENAMENTUL AGENTILOR PE BAZA EXPERIENTELOR
def train_agent(model, experiences, optimizer, batch_size=32):
    action_indices = []
    for action in experiences.actions:
        if hasattr(action, 'point'):
            # Dacă acțiunea are un punct asociat, codifică punctul
            action_indices.append(encoder.encode_point(action.point))
        else:
            # Pentru acțiuni care nu sunt asociate cu un punct, cum ar fi "pass"
            action_indices.append(encoder.num_points()-1)

    action_indices = np.array(action_indices)
    states_batch = np.array([encoder.encode(state) for state in experiences.states if isinstance(state, GameState)])
    rewards_batch = np.array(experiences.rewards)

    with tf.GradientTape() as tape:
        predictions = model(states_batch, training=True)
        loss = keras.losses.sparse_categorical_crossentropy(action_indices, predictions)
        loss = tf.reduce_mean(loss * rewards_batch)

    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))


# SETAREA NUMARULUI DE EPISOADE SI APELAREA METODELOR DE ANTRENARE
num_episodes = 5
for episode in range(num_episodes):
    print("Started episode: ", episode)
    play_game(agent_black, agent_white, board_size)
    train_agent(model_policy, collector_black.to_buffer(), optimizer_black)
    print(f"Finished episode {episode} with success!")


# SALVARE MODELE
model_policy.save('C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\black_agent_model5.h5')
# model_white.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\white_agent_model.h5')

# model.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\model3.h5')

