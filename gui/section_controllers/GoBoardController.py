from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPointF

from dlgo import gotypes


class GoBoardController(QtWidgets.QGraphicsItem):
    def __init__(self, board_size):
        super().__init__()
        self.game = None
        self.board_size = board_size

        if self.board_size == 19:
            self.margin = 73
        elif self.board_size == 9:
            self.margin = 95
        else:
            self.margin = 90

        self.cell_size = None
        self.update_cell_size()

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 1000, 1000)

    def update_cell_size(self):
        self.cell_size = round((900 - 2 * self.margin) / (self.board_size - 1))

    def paint(self, painter, option, widget):
        self.update_cell_size()

        start = self.margin
        end = 900 - self.margin
        for row in range(self.board_size):
            for col in range(self.board_size):
                # Desenarea liniilor verticale și orizontale
                painter.drawLine(start + col * self.cell_size, start, start + col * self.cell_size, end)
                painter.drawLine(start, start + row * self.cell_size, end, start + row * self.cell_size)

        # Adaugarea coordonatelor pe marginea tablei
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)

        cols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:self.board_size]

        for i in range(self.board_size):
            # Coordonatele de pe latura de sus și de jos
            # Centrare pe linie orizontală
            painter.drawText(QPointF(start + i * self.cell_size - painter.fontMetrics().width(cols[i]) / 2,
                                     start - self.margin / 2), cols[i])
            painter.drawText(QPointF(start + i * self.cell_size - painter.fontMetrics().width(cols[i]) / 2,
                                     end + self.margin / 2 + painter.fontMetrics().height()), cols[i])

            # Coordonatele din stânga și din dreapta
            # Centrare pe linie verticală
            painter.drawText(QPointF(start - self.margin / 2 - painter.fontMetrics().width(str(self.board_size - i)) / 2,
                                     start + i * self.cell_size + painter.fontMetrics().ascent() / 2),
                             str(self.board_size - i))
            painter.drawText(QPointF(end + self.margin / 2,
                                     start + i * self.cell_size + painter.fontMetrics().ascent() / 2),
                             str(self.board_size - i))

        if self.game is not None:
            board = self.game.board
            for row in range(self.board_size):
                for col in range(self.board_size):
                    stone = board.get(gotypes.Point(row + 1, col + 1))
                    if stone is not None:
                        self.draw_stone(painter, row, col, stone)


    def draw_stone(self, painter, row, col, stone):
        # Calculul centrului și razei pentru pietre
        center_x = self.margin + col * self.cell_size
        center_y = self.margin + row * self.cell_size
        radius = round(self.cell_size // 2 )
        color = QtCore.Qt.black if stone == gotypes.Player.black else QtCore.Qt.white
        painter.setBrush(QtGui.QBrush(color))
        painter.drawEllipse(QtCore.QPointF(center_x, center_y), radius, radius)

    def update_game(self, game):
        self.game = game
        self.update()
