import importlib


class Encoder:
    # Pentru suportul numelui encoderului
    def name(self):
        raise NotImplementedError()

    # Transforma tabla de Go intr-un format de date numeric
    def encode(self, game_state):
        raise NotImplementedError()

    # Transforma un punct de pe tabla intr-un format de index intreg
    def encode_point(self, point):
        raise NotImplementedError()

    # Transforma indexul intreg inapoi intr-un punct de pe tabla de Go
    def decode_point_index(self, index):
        raise NotImplementedError()

    # Numarul de puncte totale de pe tabla
    def num_points(self):
        raise NotImplementedError()

    # Forma structurii codificate
    def shape(self):
        raise NotImplementedError()

    # Aceasta functie permite crearea encoderelor folosind numele lor
    def get_encoder_by_name(name, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        module = importlib.import_module('dlgo.encoders.' + name)
        constructor = getattr(module, 'create')
        return constructor(board_size)
