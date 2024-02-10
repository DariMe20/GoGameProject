from GameRules.gotypes import Point


def is_point_an_eye(board, point, color):
    """
    Metoda care verifica daca un punct de pe tabla este un ochi al unui grup (nu vrem ca programul sa considere acel
    punct o granita si sa il acopere)
    Avem 2 cazuri de ochi:
        1 - Ochiul este in interiorul grupului (este incojurat in totalitate de piese de aceeasi culoare)
        2 - Ochiul are libertati comune cu latura sau cu coltul

    :param board: tabla de joc
    :param point: punctul de plasat
    :param color: culoarea piesei ce va fi plasata
    """
    # Un ochi este un punct gol inconjurat de piese (sau de piese si marginea tablei)
    # Un grup are nevoie de minim 2 ochi pentru a nu putea fi capturat de adversar (pentru a fi in viata)
    if board.get(point) is not None:
        return False

    # Toate piesele adiacente trebuie sa fie de aceeasi culoare
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False

    friendly_corners = 0
    off_board_corners = 0
    # Verificam diagonalele punctului
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]
    # Daca diagonelele (colturile punctului) sunt piese ale jucatorului (friendly) atunci le salvam
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    if off_board_corners > 0:
        # Verificare daca punctul este in colt sau pe margine - returneaza True daca da
        return off_board_corners + friendly_corners == 4

    # Ochiul e in mijloc (probabil are cel putin o libertate fiindca un grup poate sa aiba un ochi mai mare de 1 punct)
    return friendly_corners >= 3
