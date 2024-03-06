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
