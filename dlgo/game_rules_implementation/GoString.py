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
