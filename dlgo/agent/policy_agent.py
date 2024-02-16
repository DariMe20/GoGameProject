import h5py
import numpy as np
from keras import Sequential
from keras.src.layers import Dense, Activation
import os
import dlgo
import tensorflow as tf
from dlgo import encoders, agent, kerasutil, goboard
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.encoders.simple import SimpleEncoder
from dlgo.goboard import GameState
from dlgo.keras_networks import large_network
from dlgo.rl.experience import ExperienceBuffer
from dlgo.rl.experience_colector import ExperienceCollector

class PolicyAgent(Agent):
    def __init__(self, model, encoder):
        super().__init__()
        self.collector = None
        self._model = model
        self._encoder = encoder
        # self.color = color

    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self._encoder.name()
        h5file['encoder'].attrs['board_width'] = self._encoder.board_width
        h5file['encoder'].attrs['board_height'] = self._encoder.board_height
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self._model, h5file['model'])

    def select_move(self, game_state):
        # codificare tabla
        board_tensor = self._encoder.encode(game_state)
        X = np.array([board_tensor])

        # generare probabilitati
        move_probs = self._model.predict(X)[0]
        move_probs = clip_probs(move_probs)
        print_probs(move_probs, 9, 9)

        # preluare numar total de mutari
        num_moves = self._encoder.board_width * self._encoder.board_height

        # aranjare si alegere mutari candidat
        candidates = np.arange(num_moves)
        ranked_moves = np.random.choice(candidates, num_moves, replace=False, p=move_probs)

        # decodare mutari posibile
        for point_idx in ranked_moves:
            point = self._encoder.decode_point_index(point_idx)

            # verificare mutare
            move = goboard.Move.play(point)
            is_valid = game_state.is_valid_move(move)
            is_an_eye = is_point_an_eye(game_state.board, point, game_state.next_player)
            is_on_edge = game_state.is_move_on_edge(move)

            # alege mutarea
            if is_valid and (not is_an_eye):

                # notific collectorul ca agentul a ales o mutare
                if self.collector is not None:
                    self.collector.record_decision(
                        state=board_tensor,
                        action=point_idx
                    )

                return goboard.Move.play(point)

        # pass daca nu exista mutari valide/bune
        return goboard.Move.pass_turn()

    def set_collector(self, collector):
        self.collector = collector


def print_probs(move_probs, board_width, board_height):
    i = 0
    for row in range(board_height):
        row_formatted = []
        for col in range(board_width):
            row_formatted.append('{:.3f}'.format(move_probs[i]))
            i += 1
        print(' '.join(row_formatted))

def clip_probs(original_probs):
    min_p = 1e-5
    max_p = 1 - min_p
    clipped_probs = np.clip(original_probs, min_p, max_p)
    clipped_probs = clipped_probs / np.sum(clipped_probs)
    return clipped_probs


def load_policy_agent(h5file):
    model = kerasutil.load_model_from_hdf5_group(
        h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    board_width = h5file['encoder'].attrs['board_width']
    board_height = h5file['encoder'].attrs['board_height']
    encoder = encoders.get_encoder_by_name(
        encoder_name,
        (board_width, board_height))
    return PolicyAgent(model, encoder)

