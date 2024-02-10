from importlib import import_module


def get_encoder_by_name(name, board_size):
    if isinstance(board_size, int):
        board_size = (board_size, board_size)
    module = import_module('dlgo.encoders.' + name)
    return module.create(board_size)