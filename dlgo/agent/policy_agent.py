"""Policy gradient learning."""
import numpy as np
from keras import backend as K
from keras.optimizers import SGD
from keras.src.saving.saving_api import save_model

from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo import encoders
from dlgo import goboard
from dlgo import kerasutil

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
    def __init__(self, model, encoder):
        Agent.__init__(self)
        self._model = model
        self._encoder = encoder
        self._collector = None
        self._temperature = 0.3
        self.probs_for_gui = ""

    def predict(self, game_state):
        encoded_state = self._encoder.encode(game_state)
        input_tensor = np.array([encoded_state])
        return self._model.predict(input_tensor)[0]

    def set_temperature(self, temperature):
        self._temperature = temperature

    def set_collector(self, collector):
        self._collector = collector

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
        self.probs_for_gui = probs_for_gui(move_probs, self._encoder.board_width, self._encoder.board_height)
        return self.probs_for_gui

    def select_move(self, game_state):
        move_probs, board_tensor, num_moves = self.get_move_probs(game_state)

        # print_probs(move_probs, self._encoder.board_width, self._encoder.board_height)

        # Turn the probabilities into a ranked list of moves.
        candidates = np.arange(num_moves)
        ranked_moves = np.random.choice(candidates, num_moves, replace=False, p=move_probs)

        for point_idx in ranked_moves:
            point = self._encoder.decode_point_index(point_idx)
            if game_state.is_valid_move(goboard.Move.play(point)) \
                    and not is_point_an_eye(game_state.board,point, game_state.next_player) \
                    and not game_state.is_move_on_edge(goboard.Move.play(point)):
                if self._collector is not None:
                    self._collector.record_decision(
                        state=board_tensor,
                        action=point_idx
                    )
                return goboard.Move.play(point)
        # No legal, non-self-destructive moves less.
        return goboard.Move.pass_turn()

    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self._encoder.name()
        h5file['encoder'].attrs['board_width'] = self._encoder.board_width
        h5file['encoder'].attrs['board_height'] = self._encoder.board_height
        h5file.create_group('model')
        save_model(self._model, h5file)

    def train(self, experience, lr=0.001, clipnorm=1.0, batch_size=712):
        opt = SGD(learning_rate=lr, clipnorm=clipnorm)
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


def probs_for_gui(move_probs, board_width, board_height):
    # CSS pentru a ajusta dimensiunea și spațiul tabelei
    css_style = """
    <style>
        table {
            width: 500px;
            height: 400px;
            border: none;

        }
        td, th {
            overflow: hidden;
            font-size: 12px; 
            width:50px;
            height:50px;
            padding: 3px;
        }
        
        th{ 
            color:brown;
            font-weight: bold;
        }
    </style>
    """

    # Definim headerul cu literele A-I și creăm un tabel HTML
    letters = 'ABCDEFGHIJ'[0:board_width]  # Adaptat pentru lățimea tabelei
    header = ''.join(f'<th>{letter}</th>' for letter in letters)
    header_footer = f'<tr><th></th>{header}<th></th></tr>'

    # Începem construcția tabelului HTML
    board_html = f"<html><head>{css_style}</head><body><table><tbody>"
    board_html += header_footer  # Header cu litere

    i = 0
    for row in range(board_height, 0, -1):
        row_html = f"<tr><th>{row}</th>"  # Numărul rândului la început
        for col in range(board_width):
            mi = move_probs[i] * 100
            row_html += f'<td>{mi:.2f}%</td>'
            i += 1
        row_html += f"<th>{row}</th></tr>"  # Numărul rândului la sfârșit
        board_html += row_html

    board_html += header_footer  # Footer cu litere
    board_html += "</tbody></table></body></html>"

    return board_html
