from PyQt5 import QtWidgets, QtCore, QtGui

from dlgo import gotypes


class GoBoardController(QtWidgets.QGraphicsItem):
    def __init__(self, board_size):
        super().__init__()
        self.game = None
        self.board_size = board_size

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 900, 900)

    def paint(self, painter, option, widget):
        start = 30
        end = 840
        cell_size = round((end-start) / (self.board_size - 1))
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Desenarea liniilor verticale
                painter.drawLine(start + col*cell_size, start, start + col*cell_size, end)
                # Desenarea liniilor orizontale
                painter.drawLine(start, start + row * cell_size, end, start + row * cell_size)

        # Adaugarea coordonatelor pe marginea tablei
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        cols = 'ABCDEFGHIJKLMNOPQRST'

        for i in range(self.board_size):
            # Laturile de sus si de jos vor avea coordonate litere
            painter.drawText(start + i * cell_size - 2, start - 25, cols[i])
            painter.drawText(start + i * cell_size - 2, end + 35, cols[i])

            # Coordonatele din stânga și din dreapta
            painter.drawText(start - 35, start + i * cell_size + 2, str(self.board_size - i))
            painter.drawText(end + 33, start + i * cell_size + 2, str(self.board_size - i))

        if self.game is not None:
            board = self.game.board
            for row in range(self.board_size):
                for col in range(self.board_size):
                    stone = board.get(gotypes.Point(row + 1, col + 1))
                    if stone is not None:
                        self.draw_stone(painter, row, col, stone)

    def draw_stone(self, painter, row, col, stone):
        start = 30
        end = 840
        cell_size = round((end - start) / (self.board_size - 1))
        center_x = start + col * cell_size
        center_y = start + row * cell_size
        radius = (
            round(cell_size // 2 - 2)
        )  # mică ajustare pentru a păstra pietrele în interiorul intersecțiilor
        color = QtCore.Qt.black if stone == gotypes.Player.black else QtCore.Qt.white
        painter.setBrush(QtGui.QBrush(color))
        painter.drawEllipse(QtCore.QPointF(center_x, center_y), radius, radius)


    def update_game(self, game):
        # actualizează starea internă și re-desenează tabloul
        self.game = game
        self.update()
