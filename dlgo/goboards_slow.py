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
        self.is_play = (self.point is not None)
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
    Aceasta metoda creaza structura unui grup de piese pe tabla si se caracterizeaza prin culoarea pieselor,
    pietrele din care este compus grupul si numarul de libertati pentru a verifica statusul de viata/captura - in cod
    este reprezentat printr-un set de pozitii ce compun lista libertatilor
    """

    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
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
        return GoString(self.color, combined_stones, (self.liberties | go_string.liberties) - combined_stones)

    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
               self.color == other.color and \
               self.stones == other.stones and \
               self.liberties == other.liberties

class Board():
    def __init__(self, num_rows, num_cols):
        """
        Constructor pentru initializarea tablei de GO avand un numar specificat de randuri si coloane
        :param num_rows: numarul de randuri
        :param num_cols: numarul de coloane
        """
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}     # private variable as dictionary

    def place_stone(self, player, point):
        """
        Metoda pentru plasarea unei piese de go pe tabla
        :param player: Culoarea jucatorului care este la rand
        :param point: Punctul in care jucatorul vrea sa joace
        :return:
        """

        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []