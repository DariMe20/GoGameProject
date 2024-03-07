from dlgo.encoders.simple import SimpleEncoder
from dlgo.keras_networks.network_builder.q_value_network import QValueModel


def generate_q_network(encoder):
    q_model_object = QValueModel(encoder)
    q_model = q_model_object.build_model()
    q_model.save('./q_models/model_Q11111.h5')


board_size = 9
simple_encoder = SimpleEncoder((board_size, board_size))
