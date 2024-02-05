import cProfile
import copy
import math
import random
from GameRules import gotypes, goboard
from GameRules.agent.base import Agent


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

    def __init__(self, num_rounds=10):
        super().__init__()
        self.temperature = 1.9
        self.num_rounds = num_rounds

    @staticmethod
    def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
        if child_rollouts == 0:
            return float('inf')  # Asigură explorarea nodurilor nevizitate
        exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
        return win_pct + temperature * exploration

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
        total_rollouts = sum(child.num_rollouts for child in node.children)
        best_score = -1
        best_child = None
        for child in node.children:
            score = self.uct_score(total_rollouts,
                                   child.num_rollouts,
                                   child.winning_pct(node.game_state.next_player),
                                   self.temperature)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def heuristic_select_move(self, possible_moves, game_state):
        capture_moves = []
        extend_moves = []
        for move in possible_moves:
            if move.is_play:
                # Verifică dacă mutarea capturează pietre adversare
                if self.does_move_capture(move, game_state):
                    capture_moves.append(move)
                # Verifică dacă mutarea extinde un grup existent
                elif self.does_move_extend(move, game_state):
                    extend_moves.append(move)
        if capture_moves:
            return random.choice(capture_moves)
        elif extend_moves:
            return random.choice(extend_moves)
        else:
            return random.choice(possible_moves)

    def does_move_capture(self, move, game_state):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(game_state.board)
        next_board.place_stone(game_state.next_player, move.point)
        # Verifică dacă vreo piesă adversă rămâne fără libertăți
        for neighbor in move.point.neighbors():
            if not next_board.is_on_grid(neighbor):
                continue
            neighbor_string = next_board.get_go_string(neighbor)
            if neighbor_string is None or neighbor_string.color == game_state.next_player:
                continue
            if neighbor_string.num_liberties == 0:
                return True
        return False

    def does_move_extend(self, move, game_state):
        if not move.is_play:
            return False
        for neighbor in move.point.neighbors():
            if not game_state.board.is_on_grid(neighbor):
                continue
            neighbor_string = game_state.board.get_go_string(neighbor)
            if neighbor_string is not None and neighbor_string.color == game_state.next_player:
                # Verifică dacă mutarea extinde un grup existent al jucătorului
                return True
        return False

    def simulate_random_game(self, game_state):
        print("In simulate")
        state = game_state
        while not state.is_over():
            possible_moves = state.legal_moves()
            move = self.heuristic_select_move(possible_moves, state)
            state = state.apply_move(move)
            print("WInner is: ", state.winner())
        return (

            state.winner()
        )
