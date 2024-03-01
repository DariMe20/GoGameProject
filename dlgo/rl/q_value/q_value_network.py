from keras.layers import Input, Dense, Flatten, concatenate
from keras.models import Model
from keras.src.optimizers import Adam

from dlgo.encoders.simple import SimpleEncoder
from dlgo.keras_networks.large_network import layers

board_size = 9
encoder = SimpleEncoder((board_size, board_size))
shape = encoder.shape()
points = encoder.num_points()


def create_q_value_network(input_shape, num_points):
    board_input = Input(shape=input_shape, name='board_input')

    # Integrare layere
    x = board_input
    for layer in layers(input_shape):
        x = layer(x)

    # Flatten si un Dense pentru decizie
    flat = Flatten()(x)
    processed_board = Dense(512, activation='relu')(flat)

    # Input pentru acțiuni
    action_input = Input(shape=(num_points,), name='action_input')

    # Concatenarea output-ului procesat al tablei de joc cu input-ul de acțiuni
    board_and_action = concatenate([action_input, processed_board])

    # Un layer ascuns și definirea output-ului pentru q_values
    hidden_layer = Dense(256, activation='relu')(board_and_action)
    q_value_output = Dense(1, activation='tanh')(hidden_layer)

    # Crearea modelului
    model = Model(inputs=[board_input, action_input], outputs=q_value_output)

    return model


def build_q_model():
    q_value_model = create_q_value_network(shape, points)
    q_value_model.compile(loss='mse', optimizer=Adam(lr=0.001))
    return q_value_model


q_model = build_q_model()
q_model.save('./q_models/model_Q1.h5')