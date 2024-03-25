import numpy as np
from keras.src.optimizers import SGD
from keras.src.saving.saving_api import save_model

from agent import Agent, is_point_an_eye
from dlgo.game_rules_implementation.Move import Move


class QAgent(Agent):
    def __init__(self, model, encoder):
        super().__init__()
        self.model = model
        self._encoder = encoder
        self.collector = None
        self.temperature = 0.1
        self.compute_probs = False

    # SETTER METHODS
    def set_temperature(self, temperature):
        self.temperature = temperature

    def set_collector(self, collector):
        self.collector = collector

    # Method to implement epsilon greedy for move selection
    def rank_moves_eps_greedy(self, values):
        # temperatura reprezinta epsilon greedy
        if np.random.random() < self.temperature:
            # Explorare - ordoneaza mutarile dupa valori random, nu dupa cele reale
            values = np.random.random(values.shape)
        # Scoate indicii valorilor de la mic la mare
        ranked_moves = np.argsort(values)
        # Inverseaza vectorul
        return ranked_moves[::-1]

    # METHOD TO SELECT MOVE
    def select_move(self, game_state):
        board_tensor = self._encoder.encode(game_state)
        moves = []
        board_tensors = []

        # Genereaza o lista cu toate mutarile valide
        for move in game_state.legal_moves():
            if not move.is_play:
                continue
            moves.append(self._encoder.encode_point(move.point))
            board_tensors.append(board_tensor)

        # Agentul va zice pass daca nu exista alte mutari valide
        if not moves:
            return Move.pass_turn()

        # Formateaza mutarile
        num_moves = len(moves)
        board_tensors = np.array(board_tensors)
        move_vectors = np.zeros((num_moves, self._encoder.num_points()))
        for i, move in enumerate(moves):
            move_vectors[i][move] = 1

        values = self.model.predict([board_tensors, move_vectors])
        values = values.reshape(len(moves))

        # Ordoneaza mutarile conform epsilon greedy
        ranked_moves = self.rank_moves_eps_greedy(values)

        for move_idx in ranked_moves:
            point = self._encoder.decode_point_index(moves[move_idx])
            if not is_point_an_eye(game_state.board, point, game_state.next_player):
                if self.collector is not None:
                    self.collector.record_decision(
                        state=board_tensor,
                        action=moves[move_idx],
                    )
                return Move.play(point)
        return Move.pass_turn()

    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self._encoder.name()
        h5file['encoder'].attrs['board_width'] = self._encoder.board_width
        h5file['encoder'].attrs['board_height'] = self._encoder.board_height
        h5file.create_group('model')
        save_model(self.model, h5file)

    def train(self, experience, lr=0.1, clip_norm=1.0, batch_size=128):
        opt = SGD(learning_rate=lr)
        self.model.compile(loss='mse', optimizer=opt)

        n = experience.states.shape[0]
        # Translate the actions/rewards.
        num_moves = self._encoder.num_points()
        actions = np.zeros((n, num_moves))
        y = np.zeros((n,))

        for i in range(n):
            action = experience.actions[i]
            reward = experience.rewards[i]
            actions[i][action] = 1
            y[i] = reward

        self.model.fit(
            [experience.states, actions], y,
            batch_size=batch_size,
            epochs=2, verbose=1)
