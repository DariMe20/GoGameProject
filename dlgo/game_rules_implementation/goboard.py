import copy

import dlgo.game_rules_implementation.Player
from dlgo.game_rules_implementation import gotypes
from dlgo.game_rules_implementation.Board import Board
from dlgo.game_rules_implementation.Move import Move
from dlgo.game_rules_implementation.Point import Point
from dlgo.game_rules_implementation.Player import Player


class GameState:
    def __init__(self, board, next_player, previous, move, black_prisoners=0, white_prisoners=0, move_number=0):
        self.komi = 6.5
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.move_number = move_number

        if self.previous_state is None:
            self.previous_states = frozenset()
            self.black_prisoners = black_prisoners
            self.white_prisoners = white_prisoners
        else:
            self.previous_states = frozenset(
                previous.previous_states | {(previous.next_player, previous.board.zobrist_hash())})
            self.black_prisoners = previous.black_prisoners
            self.white_prisoners = previous.white_prisoners
            self.move_number = previous.move_number + 1

        self.last_move = move

    def apply_move(self, move):
        """
        Metoda care returneaza un nou GameState upa ce o mutare este plasata
        :param move: Mutarea efectuata - plasare piesa, cedare (resign) sau pass
        :return: GameState -  noul status al jocului
        """
        if not self.is_valid_move(move):
            return

        if move.is_play:
            next_board = copy.deepcopy(self.board)
            captured = next_board.place_stone(self.next_player, move.point)
            if self.next_player == Player.black:
                self.white_prisoners += captured
            else:
                self.black_prisoners += captured
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        """
        Metoda care initializeaza datele si tabla pentru un nou joc
        :param board_size: Dimensiunile tablei - rows = cols
        :return: GameState pentru o tabla noua
        """
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_over(self):
        """
        Metoda pentru a detecta finalizarea unui joc -  fie ambii jucatori zic pass, fie unul dintre ei cedeaza
        :return: Valoare booleana - True daca jocul e gata, False daca jocul inca continua
        """
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def is_move_self_capture(self, player, move):
        """
        In Go un jucator se poate autosabota prin plasarea unei piese pe tabla care ar duce automat la sinucidere
        Sinuciderea nu ese permisa, nu poti plasa o piesa pe tabla care ti-ar reduce libertatile la 0
        Aceasta metoda evita sinuciderea prin verificarea numarului de libertati

        :param player: Jucatorul care face mutarea
        :param move: Tipul mutarii
        :return: Valoare booleana - True daca e autocaptura, False daca nu
        """
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)

        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0

    @property
    def situation(self):
        """
        Metoda pentru a returna situatia de pe tabla
        :return: urmatorul jucator, tabla actuala
        """
        return self.next_player, self.board

    def does_move_violate_ko(self, player, move):
        """
        Ko este o situatie speciala in jocul de Go care ar putea duce la un ciclu infinit de capturi
        Aceasta metoda implementeaza o formulare cunoscuta si ca regula "situational superko" prin care nu lasa jucatorul
        actual sa captureze piesa in ko pana cand nu da o amenintare in alta parte
        Metoda foloseste proprietatea faptului ca fiecare instanta GameState pastreaza un pointer catre starea precedenta
        iar din acest motiv, se poate implementa regula de ko prin traversarea inapoi a arborlui de stari

        :param player:Jucatorul activ
        :param move: Tipul mutarii
        :return: valoare booleana - True daca mutarea nu incalca regula de Ko, False altfel
        """

        if not move.is_play:
            return False

        # Copiem tabla actuala si plasam noua piesa
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)

        # Creem urmatoare situatie de pe tabla
        next_situation = (player.other, next_board.zobrist_hash())
        if next_situation in self.previous_states:
            print("Move violates Ko")
        return next_situation in self.previous_states

    def is_valid_move(self, move):
        try:
            """
            Metoda care verifica corectitudinea unei plasari pe tabla - nu e sinucidere si nu incalca regula de ko
            :param move: tipul mutarii - plasare, reisgn, pass
            :return: valoare booleana - True daca mutarea e valida, False daca mutarea nu e valida
            """
            if self.is_over():
                return False
            if move.is_pass or move.is_resign:
                return True
            return (
                    self.board.get(move.point) is None
                    and not self.is_move_self_capture(self.next_player, move)
                    and not self.does_move_violate_ko(self.next_player, move)
            )
        except Exception as e:
            print(f"Exception in move validation method: {e}")

    def legal_moves(self):
        """
        Returnează o listă de obiecte Move care sunt mutări legale în starea curentă a jocului.
        """
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)

        # Adaugă mutări speciale, cum ar fi 'pass' și 'resign'
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves

    def winner(self):
        winner, scores = self.evaluate_territory()
        black_score = scores[Player.black] - scores[Player.white]
        white_score = scores[Player.white] - scores[Player.black]
        if black_score > 0:
            print(f"Black won by {black_score}")
            return dlgo.game_rules_implementation.Player.Player.black
        elif white_score > 0:
            print(f"White won by {white_score}")
            return dlgo.game_rules_implementation.Player.Player.white
        else:
            return None

    def evaluate_territory(self):
        black_score = 0
        white_score = 0
        total_points = self.board.num_rows * self.board.num_cols
        half_total_points = total_points / 2
        komi = self.komi

        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                point = Point(row, col)
                stone = self.board.get(point)
                if stone == Player.black:
                    black_score += 1
                elif stone == Player.white:
                    white_score += 1
                else:
                    # Dacă punctul este liber, determină cui aparține teritoriul
                    territory, borders = self.collect_territory(self.board, point)
                    if len(borders) == 1:
                        player_border = borders.pop()
                        if player_border == Player.black:
                            black_score += len(territory)
                        elif player_border == Player.white:
                            white_score += len(territory)

        adjusted_black_score = black_score - komi / 2
        adjusted_white_score = total_points - adjusted_black_score

        if adjusted_black_score > half_total_points:
            winner = "Black wins by " + str(adjusted_black_score - adjusted_white_score) + " points"
        else:
            winner = "White wins by " + str(adjusted_white_score - adjusted_black_score) + " points"

        return winner, {
            Player.black: adjusted_black_score,
            Player.white: adjusted_white_score,
        }

    def collect_territory(self, board, start_point):
        territory = set()
        borders = set()
        queue = [start_point]
        visited = set([start_point])

        while queue:
            point = queue.pop()
            neighbors = point.neighbors()
            territory.add(point)

            for neighbor in neighbors:
                if not board.is_on_grid(neighbor):
                    continue
                neighbor_stone = board.get(neighbor)
                if neighbor_stone is None:
                    if neighbor not in visited:
                        queue.append(neighbor)
                        visited.add(neighbor)
                else:
                    borders.add(neighbor_stone)

        return territory, borders

    def find_atari_groups(self, color):
        """
        Identifică grupurile de pietre de o anumită culoare care sunt în Atari.

        :param board: Instanța curentă a tablei de joc.
        :param color: Culoarea grupurilor de pietre de verificat.
        :return: O listă de tuple, fiecare conținând un GoString reprezentând grupul în Atari și punctul său de libertate.
        """
        atari_groups = []
        for point, go_string in self.board.grid.items():
            if go_string is None:
                return
            if go_string.color == color and go_string.num_liberties == 1:
                liberty = next(iter(go_string.liberties))  # obține singura libertate a grupului
                atari_groups.append((go_string, liberty))
        return atari_groups

    def atari_places(self, color):
        """
        Identifică punctele unde pietrele adversarului de o anumită culoare sunt în Atari și pot fi capturate.

        :param color: Culoarea pietrelor agentului cu care jucam
        :return: O listă de puncte unde pietrele de culoarea specificată pot fi capturate.
        """
        # Identifică culoarea adversarului
        opponent_color = dlgo.game_rules_implementation.Player.Player.black if color == dlgo.game_rules_implementation.Player.Player.white else dlgo.game_rules_implementation.Player.Player.white

        # Găsește grupurile adversarului care sunt în Atari
        atari_groups = self.find_atari_groups(opponent_color)

        if atari_groups:
            # Extrag punctele de libertate ale grupurilor în Atari, care reprezintă locațiile de capturare
            capture_points = [liberty for _, liberty in atari_groups]
            return capture_points
        else:
            return None

    def is_move_on_edge(self, move):
        """
        Verifică dacă o mutare este pe marginea tablei de joc.

        :param move: Instanța mutării care va fi verificată.
        :return: True dacă mutarea este pe margine, altfel False.
        """
        if not move.is_play or self.move_number >= 35:
            return False  # Pas și cedare nu sunt considerate pe margine

        # Verifică dacă mutarea este pe prima sau ultima linie/coloană
        # print(f"move:{move}=  row: {move.point.row}   col:{move.point.col}")
        is_on_edge_row = move.point.row == 1 or move.point.row == self.board.num_rows
        is_on_edge_col = move.point.col == 1 or move.point.col == self.board.num_cols

        return is_on_edge_row or is_on_edge_col

    def is_move_atari(self, move):
        if not move.is_play:
            return False
        # Simulează mutarea
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(self.next_player, move.point)
        # Verifică dacă vreun grup advers are o singură libertate
        for neighbor in move.point.neighbors():
            if not next_board.is_on_grid(neighbor):
                continue
            neighbor_string = next_board.get_go_string(neighbor)
            if neighbor_string is None:
                continue
            if neighbor_string.color != self.next_player and neighbor_string.num_liberties == 1:
                return True
        return False

    def is_move_protect(self, move):
        if not move.is_play:
            return False

        # Find friendly strings next to the move point that are in Atari.
        at_risk_groups = [
            self.board.get_go_string(neighbor)
            for neighbor in move.point.neighbors()
            if self.board.is_on_grid(neighbor) and
               self.board.get_go_string(neighbor) and
               self.board.get_go_string(neighbor).color == self.next_player and
               self.board.get_go_string(neighbor).num_liberties == 1
        ]

        # Simulate the move
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(self.next_player, move.point)

        # Check if any at-risk group now has more liberties
        for group in at_risk_groups:
            # You have to find the corresponding group on the new board
            new_group = next_board.get_go_string(list(group.stones)[0])
            if new_group and new_group.num_liberties > 1:
                return True

        return False


    def is_move_capture(self, move):
        if not move.is_play or not self.is_valid_move(move):
            return False
        original_board = copy.deepcopy(self.board)
        captured_stones = original_board.place_stone(self.next_player, move.point)
        return captured_stones > 0


    def is_move_reducing_opponent_liberties(self, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(self.next_player, move.point)
        for neighbor in move.point.neighbors():
            if not next_board.is_on_grid(neighbor):
                continue
            neighbor_string = next_board.get_go_string(neighbor)
            if neighbor_string is None or neighbor_string.color == self.next_player:
                continue
            if neighbor_string.num_liberties < self.board.get_go_string(neighbor).num_liberties:
                return True
        return False






