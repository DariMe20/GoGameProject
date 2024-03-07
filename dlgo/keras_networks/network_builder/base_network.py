class LearningModel:

    def __init__(self, encoder):
        self.encoder = encoder
        pass

    def create_network(self, shape, points):
        raise NotImplementedError()

    def build_model(self):
        raise NotImplementedError()
