import enum


class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        """
        Metoda folosita pentru a schimba jucatorii de la o mutare la alta

        :return: Culoarea jucatorului care urmeaza sa joace
        """
        return Player.black if self == Player.white else Player.white
