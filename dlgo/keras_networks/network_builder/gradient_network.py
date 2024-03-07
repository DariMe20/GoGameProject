from keras import Sequential
from keras.src.layers import Dense, Activation
from keras.src.optimizers import SGD

from dlgo.keras_networks.large_network import layers
from dlgo.keras_networks.network_builder.base_network import LearningModel


class GradientModel(LearningModel):
    def __init__(self, simple_encoder):
        super().__init__(simple_encoder)
        self.encoder = simple_encoder
        self.shape = self.encoder.shape()
        self.points = self.encoder.num_points()

    def create_network(self, shape, num_points):
        model = Sequential()
        for layer in layers(shape):
            model.add(layer)

        model.add(Dense(num_points))
        model.add(Activation('softmax'))
        return model

    def build_model(self):
        gradient_model = self.create_network(self.shape, self.points)
        optimizer = SGD()
        gradient_model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        return gradient_model
