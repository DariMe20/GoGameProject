from dlgo.game_rules_implementation.GoString import GoString
from dlgo.game_rules_implementation.Point import Point
from utils import zobrist


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
