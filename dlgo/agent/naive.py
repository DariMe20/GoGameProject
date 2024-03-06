import random
from dlgo.agent.base import Agent
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from dlgo.agent.helpers import is_point_an_eye
from dlgo.game_rules_implementation.goboard import Move
=======
=======
>>>>>>> 603e82c (Moved helpers.py in utils)
=======
>>>>>>> 603e82c (Moved helpers.py in utils)
from utils.helpers import is_point_an_eye
from dlgo.game_rules_implementation.goboards_slow import Move
>>>>>>> 603e82c (Moved helpers.py in utils)
from dlgo.game_rules_implementation.gotypes import Point


class RandomBot(Agent):
    def __init__(self, compute_probs=False):
        super().__init__()
        self.compute_probs = compute_probs

    def select_move(self, game_state):
        """Choose a random valid move that preserves our own eyes."""
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if (game_state.is_valid_move(Move.play(candidate))
                        and not is_point_an_eye(game_state.board, candidate, game_state.next_player)):
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))
