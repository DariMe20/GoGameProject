from collections import namedtuple


class Point(namedtuple('Point', 'row col')):
    """
    Clasa care foloseste namedtuple pentru a reprezenta punctele de pe tabla si coordonatele lor
    """
    def neighbors(self):
        """
        Metoda care returneaza cele 4 puncte din jurul unui punct folosind tuple in loc de coordonate precum point[0]

        :return: Lista cu cele 4 puncte care inconjoara un singur punct de pe tabla
        """
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1)
        ]
