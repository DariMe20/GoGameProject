from dlgo.encoders.simple import SimpleEncoder
from dlgo.keras_networks.network_builder.gradient_network import GradientModel
from dlgo.keras_networks.network_builder.q_value_network import QValueModel


def generate_q_network(encoder):
    q_model_object = QValueModel(encoder)
    q_model = q_model_object.build_model()
    q_model.save('../dlgo/rl/q_value/q_models/model_QTest.h5')


def generate_gradient_network(encoder):
    gradient_model_object = GradientModel(encoder)
    gradient_model = gradient_model_object.build_model()
    gradient_model.save('../dlgo/rl/gradient_descent/gradient_descent_models/model_GradientTest.h5')


def select_model_to_generate(model):
    board_size = 9
    simple_encoder = SimpleEncoder((board_size, board_size))

    if model == "QValueModel":
        generate_q_network(simple_encoder)
    elif model == "GradientModel":
        generate_gradient_network(simple_encoder)


# This will create a network only if the empty string is completed with "QvalueModel" for q_value or "GradientModel" for gradient
select_model_to_generate("")
