from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPointF

from dlgo import gotypes


class GoBoardController(QtWidgets.QGraphicsItem):
    def __init__(self, board_size):
        super().__init__()
        self.game = None
        self.board_size = board_size

        if self.board_size == 9:
            self.margin = 56
        elif self.board_size == 13:
            self.margin = 48
        else:
            self.margin = 47

        self.view_size = 850 # Dimensiunea zonei de vizualizare grafică
        self.cell_size = None
        self.update_cell_size()


    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.view_size, self.view_size)

    def update_cell_size(self):
        self.cell_size = round((self.view_size - 2 * self.margin) / (self.board_size - 1))

    def paint(self, painter, option, widget):
        start = self.margin
        end = self.view_size - self.margin

        # Draw the Go board grid lines only
        for row in range(self.board_size):
            for col in range(self.board_size):
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
                                     0), cols[i])
            painter.drawText(QPointF(start + i * self.cell_size - painter.fontMetrics().width(cols[i]) / 2,
                                     end+self.margin+10), cols[i])

            # Coordonatele din stânga și din dreapta
            # Centrare pe linie verticală
            painter.drawText(QPointF(0, start + i * self.cell_size + painter.fontMetrics().ascent() / 2),
                             str(self.board_size - i))
            painter.drawText(QPointF(end+self.margin,
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
        radius = round(self.cell_size // 2)
        color = QtCore.Qt.black if stone == gotypes.Player.black else QtCore.Qt.white
        painter.setBrush(QtGui.QBrush(color))
        painter.drawEllipse(QtCore.QPointF(center_x, center_y), radius, radius)

    def update_game(self, game):
        self.game = game
        self.update()

