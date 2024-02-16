import copy

from dlgo import zobrist, gotypes
from dlgo.gotypes import Player, Point


class Move:
    """
    Clasa Move incorporeaza 3 tipuri de miscari:
        play - mutare pe tabla
        pass - jucatorul zice pass, adica nu vrea sa mai joace
        resign - jucatorul cedeaza jocul, adica se declara invins
    """

    def __init__(self, point=None, is_pass=False, is_resign=False):
        # Verifica faptul ca se executa un singur tip de mutare per runda
        assert (point is not None) ^ is_pass ^ is_resign

        # Initializari
        self.point = point
        self.is_play = self.point is not None
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        """
        Methoda pentru generarea unei mutari pe tabla

        :param point: Pozitia unde jucatorul vrea sa joace pe tabla
        :return: Obiect Move cu caracteristica de mutare: Play
        """

        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        """
        Metoda pentru a zice pas (daca jucatorul considera ca nu mai sunt mutari de jucat pe tabla)

        :return: Obiect Move cu caracteristica de mutare: Pass
        """
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        """
        Metoda pentru a ceda partida adversarului (jucatorul se declara invins)

        :return: Obiect Move cu caracteristica de mutare: Resign
        """
        return Move(is_resign=True)


class GoString:
    """
    Aceasta clasa creaza structura unui grup de piese pe tabla ce se caracterizeaza prin culoarea pieselor,
    pietrele din care este compus grupul si numarul de libertati pentru a verifica statusul de viata/captura - in cod
    este reprezentat printr-un set de pozitii ce compun lista libertatilor
    """

    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    def without_liberty(self, point):
        """
        Metoda pentru a indeparta libertatile unei piese de pe tabla

        :param point: punctul care va genera indepartarea unei libertati pentru un GoString
        """
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point):
        """
        Metoda pentru a adauga o libertate unui GoString  de pe tabla

        :param point: punctul care va genera adaugarea  unei libertati pentru un GoString
        """
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    def merged_with(self, go_string):
        """
        Metoda care creeaza un singur grup de piese din 2 grupuri care se unesc in timpul jocului
        Metoda verifica daca grupul care se uneste de grupul actual are aceeasi culoare, daca exista piese comune,
        le ignora de la calculul libertatilor si genereaza un nou set de libertati comune

        :param go_string: Un grup nou de piese care se alipeste la grupul actual
        :return: Obiect nou de tip GoString format prin unirea celor doua grupuri
        """
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and self.color == other.color and self.stones == other.stones \
               and self.liberties == other.liberties


class Board:
    def __init__(self, num_rows, num_cols):
        """
        Constructor pentru initializarea tablei de GO avand un numar specificat de randuri si coloane
        :param num_rows: numarul de randuri
        :param num_cols: numarul de coloane
        """
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}  # private variable as dictionary
        self._hash = zobrist.EMPTY_BOARD

    def get_grid(self):
        return self._grid

    def place_stone(self, player, point):
        """
        Metoda pentru plasarea unei piese de go pe tabla
        :param player: Culoarea jucatorului care este la rand
        :param point: Punctul in care jucatorul vrea sa joace
        :return:
        """

        # Verificare daca mutarea e pe tabla si ca punctul nu e deja ocupat de alta piesa
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        # Initializare puncte vecine mutarii
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        captured_stones = 0

        # Luam fiecare punct vecin punctului pe care vrem sa il plasam
        for neighbor in point.neighbors():
            # Daca punctul vecin nu e pe tabla, continua (piesa de mutat e in colt/pe latura)
            if not self.is_on_grid(neighbor):
                continue

            # Acum vreau sa salvez acele puncte de pe tabla neocupate care reprezinta libertatile piesei plasate
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)

            # Creem grupuri de pise de culori comune si le facem GoString daca piesa plasata se conecteaza de alte piese
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)

        new_string = GoString(player, [point], liberties)

        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)

        # Actiune 1: Uneste orice piese adiacente intr-un singur grup de piese de aceeasi culoare
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string

        self._hash ^= zobrist.HASH_CODE[point, player]

        # Actiune 2: Reduce libertatile pentru grupurile de piese de culoare opusa care au libertati comune
        for other_color_string in adjacent_opposite_color:
            replacement = other_color_string.without_liberty(point)
            if replacement.num_liberties:
                self._replace_string(other_color_string.without_liberty(point))
            else:
                self._remove_string(other_color_string)

        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 1:
                captured_stones += len(other_color_string.stones)  # Adaugă numărul de pietre capturate
                self._remove_string(other_color_string)

        return captured_stones

    def _replace_string(self, new_string):
        for point in new_string.stones:
            self._grid[point] = new_string

    def is_on_grid(self, point):
        """
        Metoda se asigura ca piesa ce va fi mutata e in interiorul tablei de joc

        :return: boolean: True daca piesa e in interiorul tablei, False daca nu
        """

        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get(self, point):
        """
        Metoda care returneaza continutul unui punct de pe tabla

        :param point: Punctul ce va fi plasat pe tabla
        :return: Continutul unui punct de pe tabla: Culoarea jucatorului daca pozitia e jucata, None daca nu
        """
        string = self._grid.get(point)

        if string is None:
            return None
        return string.color

    def get_go_string(self, point):
        """
        Metoda care returneaza intregul sir de piese de aceeasi culoare (grup) asociat unui punct pe tabla
        :param point: Punctul ce va fi plasat pe tabla
        :return: Un grup de piese din care face parte punctul analizat, daca nu exista, atunci None
        """
        string = self._grid.get(point)
        if string:
            return string

    def _remove_string(self, string):
        """
        Metoda care realizeaza captura pe tabla - atunci cand o piesa sau un grup de piese isi pierde toate libertatile,
        acele piese sunt indepartate de pe tabla si devin prizonierii adversarului

        :param string: String-ul de piese care va fi indepartat (1 sau mai multe piese)
        """
        num_captured = len(string.stones)
        # Parcurg pietrele din grup
        for point in string.stones:
            # !! OBS: Indepartarea unui grup de piese genereaza libertati suplimentare pentru grupurile din jur
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.with_liberty(point))
            self._grid[point] = None

            self._hash ^= zobrist.HASH_CODE[point, string.color]
        return num_captured

    def count_stones(self, player):
        """
        Numără pietrele pe tablă pentru un jucător specific.

        :param player: Jucătorul pentru care se numără pietrele.
        :return: Numărul de pietre ale jucătorului pe tablă.
        """
        count = 0
        for row in range(1, self.num_rows + 1):
            for col in range(1, self.num_cols + 1):
                point = Point(row, col)
                if self.get(point) == player:
                    count += 1
        return count

    def zobrist_hash(self):
        return self._hash


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
            return gotypes.Player.black
        elif white_score > 0:
            print(f"White won by {white_score}")
            return gotypes.Player.white
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
            winner = "Black wins by " + str(adjusted_black_score - half_total_points) + " points"
        else:
            winner = "White wins by " + str(adjusted_white_score - half_total_points) + " points"

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
        opponent_color = gotypes.Player.black if color == gotypes.Player.white else gotypes.Player.white

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






