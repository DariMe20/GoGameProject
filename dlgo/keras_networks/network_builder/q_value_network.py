from keras.layers import Input, Dense, Flatten, concatenate
from keras.models import Model
from keras.src.optimizers import Adam

from dlgo.keras_networks.large_network import layers
from dlgo.keras_networks.network_builder.base_network import LearningModel


class QValueModel(LearningModel):
    def __init__(self, simple_encoder):
        super().__init__(simple_encoder)
        self.encoder = simple_encoder
        self.shape = self.encoder.shape()
        self.points = self.encoder.num_points()

    def create_network(self, input_shape, num_points):
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

        # Dense layer cu activare tip tanh pentru ca Q(s,a) sa fie intre [-1, 1]
        q_value_output = Dense(1, activation='tanh')(hidden_layer)

        # Crearea modelului
        model = Model(inputs=[board_input, action_input], outputs=q_value_output)

        return model

    def build_model(self):
        q_value_model = self.create_network(self.shape, self.points)
        q_value_model.compile(loss='mse', optimizer=Adam(lr=0.001))
        return q_value_model
