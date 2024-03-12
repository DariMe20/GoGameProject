"""Policy gradient learning."""
import numpy as np
from keras import backend as K
from keras.optimizers import SGD
from keras.src.saving.saving_api import save_model

import dlgo.game_rules_implementation.Move
from agent.base import Agent
from dlgo import encoders
from dlgo.keras_networks import kerasutil
from utils import utils
from utils.helpers import is_point_an_eye

__all__ = [
    'PolicyAgent',
    'load_policy_agent',
    'policy_gradient_loss',
    ]


# Keeping this around so we can read existing agents. But from now on
# we'll use the built-in crossentropy loss.
def policy_gradient_loss(y_true, y_pred):
    clip_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
    loss = -1 * y_true * K.log(clip_pred)
    return K.mean(K.sum(loss, axis=1))


def normalize(x):
    total = np.sum(x)
    return x / total


class PolicyAgent(Agent):
    """An agent that uses a deep policy network to select moves."""

    def __init__(self, model, encoder, compute_probs=True):
        Agent.__init__(self)
        self._model = model
        self._encoder = encoder
        self.collector = None
        self._temperature = 0.4
        self.probs_for_gui = ""
        self.compute_probs = compute_probs

    def predict(self, game_state):
        encoded_state = self._encoder.encode(game_state)
        input_tensor = np.array([encoded_state])
        return self._model.predict(input_tensor)[0]

    def set_temperature(self, temperature):
        self._temperature = temperature

    def set_collector(self, collector):
        self.collector = collector

    def get_move_probs(self, game_state):
        num_moves = self._encoder.board_width * self._encoder.board_height

        board_tensor = self._encoder.encode(game_state)
        x = np.array([board_tensor])

        if np.random.random() < self._temperature:
            # Explore random moves.
            move_probs = np.ones(num_moves) / num_moves
        else:
            # Follow our current policy.
            move_probs = self._model.predict(x)[0]

        # Prevent move probs from getting stuck at 0 or 1.
        eps = 1e-5
        move_probs = np.clip(move_probs, eps, 1 - eps)
        # Re-normalize to get another probability distribution.
        move_probs = move_probs / np.sum(move_probs)

        return move_probs, board_tensor, num_moves

    def generate_gui_formatted_probs(self, game_state):
        move_probs, board_tensor, num_moves = self.get_move_probs(game_state)

        # print_probs(move_probs, self._encoder.board_width, self._encoder.board_height)
        self.probs_for_gui = utils.probs_for_gui(move_probs, self._encoder.board_width, self._encoder.board_height)
        return self.probs_for_gui

    def select_move(self, game_state):
        move_probs, board_tensor, num_moves = self.get_move_probs(game_state)

        # print_probs(move_probs, self._encoder.board_width, self._encoder.board_height)

        # Turn the probabilities into a ranked list of moves.
        candidates = np.arange(num_moves)
        ranked_moves = np.random.choice(candidates, num_moves, replace=False, p=move_probs)

        for point_idx in ranked_moves:
            point = self._encoder.decode_point_index(point_idx)
            if game_state.is_valid_move(dlgo.game_rules_implementation.Move.Move.play(point)) \
                    and not is_point_an_eye(game_state.board, point, game_state.next_player) \
                    and not game_state.is_move_on_edge(dlgo.game_rules_implementation.Move.Move.play(point)):
                if self.collector is not None:
                    self.collector.record_decision(
                        state=board_tensor,
                        action=point_idx
                        )
                return dlgo.game_rules_implementation.Move.Move.play(point)
        # No legal, non-self-destructive moves less.
        return dlgo.game_rules_implementation.Move.Move.pass_turn()

    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self._encoder.name()
        h5file['encoder'].attrs['board_width'] = self._encoder.board_width
        h5file['encoder'].attrs['board_height'] = self._encoder.board_height
        h5file.create_group('model')
        save_model(self._model, h5file)

    def train(self, experience, lr, clip_norm, batch_size):
        opt = SGD(learning_rate=lr, clipnorm=clip_norm)
        self._model.compile(loss='categorical_crossentropy', optimizer=opt)

        n = experience.states.shape[0]
        # Translate the actions/rewards.
        num_moves = self._encoder.board_width * self._encoder.board_height
        y = np.zeros((n, num_moves))
        for i in range(n):
            action = experience.actions[i]
            reward = experience.rewards[i]
            y[i][action] = reward

        self._model.fit(
            experience.states, y,
            batch_size=batch_size,
            epochs=1)


def load_policy_agent(h5file):
    model = kerasutil.load_model_from_hdf5_group(
        h5file['model'],
        custom_objects={'policy_gradient_loss': policy_gradient_loss})
    encoder_name = h5file['encoder'].attrs['name']
    if not isinstance(encoder_name, str):
        encoder_name = encoder_name.decode('ascii')
    board_width = h5file['encoder'].attrs['board_width']
    board_height = h5file['encoder'].attrs['board_height']
    encoder = encoders.get_encoder_by_name(
        encoder_name,
        (board_width, board_height))
    return PolicyAgent(model, encoder)


# Afișează probabilitățile într-un format lizibil
def print_probs(move_probs, board_width, board_height):
    i = 0
    for row in range(board_height):
        row_formatted = []
        for col in range(board_width):
            mi = move_probs[i] * 100
            row_formatted.append('{:.2f}'.format(mi) + "%")
            i += 1
        print(' '.join(row_formatted))