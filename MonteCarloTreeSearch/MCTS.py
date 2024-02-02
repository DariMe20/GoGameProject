import math
import random
from dlgo import gotypes
from dlgo.agent.base import Agent


class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            gotypes.Player.black: 0,
            gotypes.Player.white: 0,
        }
        self.num_rollouts = 100
        self.children = []
        self.unvisited_moves = game_state.legal_moves()

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_over()

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)

    @staticmethod
    def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
        exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
        return win_pct + temperature * exploration


class MCTSAgent(Agent):
    def __init__(self, num_rounds):
        super().__init__()
        self.temperature = 1.2
        self.num_rounds = num_rounds

    def select_moveMCTS(self, game_state):
        root = MCTSNode(game_state)
        for i in range(self.num_rounds):
            node = root
            while not node.can_add_child() and not node.is_terminal():
                node = self.select_child(node)
            if node.can_add_child():
                node = node.add_random_child()
            winner = self.simulate_random_game(node.game_state)
            while node is not None:
                node.record_win(winner)
                node = node.parent
        # Alege cea mai bună mutare bazată pe rezultatele simulărilor
        return self.choose_best_move(root)

    def choose_best_move(self, root):
        best_move = None
        best_win_pct = -1.0
        for child in root.children:
            child_win_pct = child.winning_frac(root.game_state.next_player)
            if child_win_pct > best_win_pct:
                best_win_pct = child_win_pct
                best_move = child.move
        return best_move

    def select_child(self, node):
        best_score = -1
        best_child = None
        for child in node.children:
            # Utilizează winning_frac în loc de winning_pct
            win_rate = child.winning_frac(node.game_state.next_player)
            exploration_factor = math.sqrt(math.log(node.num_rollouts) / child.num_rollouts)
            ucb_score = win_rate + self.temperature * exploration_factor
            if ucb_score > best_score:
                best_score = ucb_score
                best_child = child
        return best_child
    def simulate_random_game(self, game_state):
        state = game_state
        while not state.is_over():
            possible_moves = state.legal_moves()
            move = random.choice(possible_moves)
            state = state.apply_move(move)
        return (
            state.winner()
        )  # presupunând că GameState are o metodă winner() care determină câștigătorul

