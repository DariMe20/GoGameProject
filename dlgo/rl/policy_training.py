import numpy as np
import tensorflow as tf
from keras.src.regularizers import l2
from keras.src.saving.saving_api import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import Adam
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
model_white = Sequential()
for layer in large_network.layers(encoder.shape()):
    model_policy.add(layer)
    model_white.add(layer)
model_policy.add(Dense(encoder.num_points(), kernel_regularizer=l2(0.001)))
model_policy.add(Dropout(0.5))
model_policy.add(Activation('softmax'))
model_white.add(Dense(encoder.num_points()))
model_white.add(Activation('softmax'))
model_path_predict = 'C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\model2.h5'
model_path_policy = 'C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\black_agent_model2.h5'
model_predict = load_model(model_path_predict)
# model_policy = load_model(model_path_policy)

# Initializare agenti pe 2 culori si colectori de experienta
agent_black = PolicyAgent(model_policy, encoder, color=Player.black)
agent_white = DeepLearningAgent(model_predict, encoder)
collector_black = ExperienceCollector()
collector_white = ExperienceCollector()
agent_black.set_collector(collector_black)
# agent_white.set_collector(collector_white)

#INITIALIZARE OPTIMIZATORI
optimizer_black = Adam(learning_rate=0.001)
optimizer_white = Adam(learning_rate=0.005)
lr_scheduler_black = tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=10, min_lr=0.0001, verbose=1)


optimizer_black.build(model_policy.trainable_variables)
# optimizer_white.build(model_white.trainable_variables)

# METODA PENTRU JOC SI COLECTARE A EXPERIENTELOR
def play_game(agent_black, agent_white, board_size):
    state = GameState.new_game(board_size)
    agents = {Player.black: agent_black, Player.white: agent_white}
    while not state.is_over():
        next_player = state.next_player
        agent_next = agents[next_player]
        move = agent_next.select_move(state)
        state = state.apply_move(move)

    winner = state.winner()
    if winner is not None:
        if winner == Player.black:
            #print("Black won!")
            collector_black.complete_episode(10)
            # collector_white.complete_episode(-1)
        else:
            #print("White won!")
            collector_black.complete_episode(0)
            # collector_white.complete_episode(1)
    else:
        collector_black.complete_episode(0)
        # collector_white.complete_episode(0)

    if state.black_prisoners < state.white_prisoners:
        collector_black.complete_episode(30)
    elif state.black_prisoners > state.white_prisoners:
        collector_black.complete_episode(-100)


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
        loss = tf.keras.losses.sparse_categorical_crossentropy(action_indices, predictions)
        loss = tf.reduce_mean(loss * rewards_batch)

    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))



# SETAREA NUMARULUI DE EPISOADE SI APELAREA METODELOR DE ANTRENARE
num_episodes = 5
for episode in range(num_episodes):
    print("Started episode: ", episode)
    play_game(agent_black, agent_white, board_size)
    train_agent(model_policy, collector_black.to_buffer(), optimizer_black)

    # train_agent(model_white, collector_white.to_buffer(), optimizer_white)
    print(f"Finished episode {episode} with success!")
callbacks = [lr_scheduler_black, tf.keras.callbacks.EarlyStopping(monitor='loss', patience=20, restore_best_weights=True)]
print(callbacks)
# SALVARE MODELE
model_policy.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\black_agent_model3.h5')
# model_white.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\white_agent_model.h5')

# model.save('C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\model3.h5')

