import numpy as np
import random

from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo import encoders, utils
from dlgo import goboard
from dlgo import kerasutil


class DeepLearningAgent(Agent):
    def __init__(self, model, encoder):
        Agent.__init__(self)
        self.probs_for_gui = None
        self.model = model
        self.encoder = encoder

    def predict(self, game_state):
        encoded_state = self.encoder.encode(game_state)
        input_tensor = np.expand_dims(encoded_state, axis=-1)

        return self.model.predict(input_tensor)[0]

    def get_move_probs(self, game_state):
        num_moves = self.encoder.board_width * self.encoder.board_height
        move_probs = self.predict(game_state)

        move_probs **= 2
        eps = 1e-6
        # Previne probabilitatile sa se blocheze la 0 sau 1
        move_probs = np.clip(move_probs, eps, 1 - eps)
        move_probs = move_probs / np.sum(move_probs)

        moves = [self.encoder.decode_point_index(i) for i in range(num_moves)]
        chosen_move = random.choices(moves, weights=move_probs)[0]

        return move_probs, chosen_move, num_moves

    def generate_gui_formatted_probs(self, game_state):
        move_probs, board_tensor, num_moves = self.get_move_probs(game_state)

        # print_probs(move_probs, self._encoder.board_width, self._encoder.board_height)
        self.probs_for_gui = utils.probs_for_gui(move_probs, self.encoder.board_width, self.encoder.board_height)
        return self.probs_for_gui

    def select_move(self, game_state):
        try:
            move_probs, chosen_move, num_moves = self.get_move_probs(game_state)

            if game_state.is_valid_move(goboard.Move.play(chosen_move)) and \
                    not is_point_an_eye(game_state.board, chosen_move, game_state.next_player):
                return goboard.Move.play(chosen_move)

            # Dacă cea mai probabilă mutare nu este validă, alege următoarea cea mai probabilă mutare
            # Prin sortarea probabilităților în ordine descrescătoare și verificarea fiecărei mutări
            for idx in np.argsort(move_probs)[::-1]:
                point = self.encoder.decode_point_index(idx)
                if game_state.is_valid_move(goboard.Move.play(point)) and \
                        not is_point_an_eye(game_state.board, point,
                                            game_state.next_player):
                    return goboard.Move.play(point)

            # Dacă nicio mutare validă nu este găsită, returnează o pasare
            return goboard.Move.pass_turn()
        except Exception as e:
            print(f"An error occurend in select_move: {e}")

    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['board_width'] = self.encoder.board_width
        h5file['encoder'].attrs['board_height'] = self.encoder.board_height
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])


def load_prediction_agent(h5file):
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    if not isinstance(encoder_name, str):
        encoder_name = encoder_name.decode('ascii')
    board_width = h5file['encoder'].attrs['board_width']
    board_height = h5file['encoder'].attrs['board_height']
    encoder = encoders.get_encoder_by_name(
        encoder_name, (board_width, board_height))
    return DeepLearningAgent(model, encoder)