import cProfile
import copy
import math
import random
from dlgo import gotypes, goboard, agent
from dlgo.agent import naive
from dlgo.agent.base import Agent
from dlgo.agent.naive import RandomBot
from dlgo.gotypes import Player


class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            gotypes.Player.black: 0,
            gotypes.Player.white: 0,
        }
        self.num_rollouts = 0
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


class MCTSAgent(Agent):

    def __init__(self, model, encoder, num_rounds=1, temperature=0.1, compute_probs=False):
        super().__init__()
        self.model = model
        self.encoder = encoder
        self.temperature = temperature
        self.num_rounds = num_rounds
        self.compute_probs = compute_probs

    @staticmethod
    def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
        if child_rollouts == 0:
            return float('inf')  # Asigură explorarea nodurilor nevizitate
        exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
        return win_pct + temperature * exploration

    def select_move(self, game_state):
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
        total_rollouts = sum(child.num_rollouts for child in node.children)
        best_score = -1
        best_child = None
        for child in node.children:
            win_pct = child.winning_frac(node.game_state.next_player)
            score = self.uct_score(total_rollouts,
                                   child.num_rollouts,
                                   win_pct,
                                   self.temperature)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def simulate_random_game(self, game_state):
        state = game_state
        bots = {
            Player.black: naive.RandomBot(),
            Player.white: naive.RandomBot(),
        }
        while not state.is_over():
            bot_move = bots[state.next_player].select_move(state)
            state = state.apply_move(bot_move)
        return state.winner()
