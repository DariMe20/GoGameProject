import copy
from dlgo.gotypes import Player


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
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        """
        Metoda pentru a indeparta libertatile unei piese de pe tabla

        :param point: punctul care va genera indepartarea unei libertati pentru un GoString
        """
        self.liberties.remove(point)

    def add_liberty(self, point):
        """
        Metoda pentru a adauga o libertate unui GoString  de pe tabla

        :param point: punctul care va genera adaugarea  unei libertati pentru un GoString
        """
        self.liberties.add(point)

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
        
        # Actiune 2: Reduce libertatile pentru grupurile de piese de culoare opusa care au libertati comune
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        
        # Actiune 3: Daca exista piese cu 0 libertati - indeparteaza => CAPTURA
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)


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

        # Parcurg pietrele din grup
        for point in string.stones:
            # !! OBS: Indepartarea unui grup de piese genereaza libertati suplimentare pentru grupurile din jur
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)

            # Indeparteaza piesa
            self._grid[point] = None


class GameState:
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):
        """
        Metoda care returneaza un nou GameState upa ce o mutare este plasata
        :param move: Mutarea efectuata - plasare piesa, cedare (resign) sau pass
        :return: GameState -  noul status al jocului
        """
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
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
        next_situation = (player.other, next_board)
        past_state = self.previous_state

        # Incercam sa verificam ca la fiecare mutare in care ko-ul este inca activ, unul dintre jucatori nu incearca sa
        # realizeze capturi succesive in acelasi ko
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
        return False

    def is_valid_move(self, move):
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
