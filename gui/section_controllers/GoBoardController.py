from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPointF, pyqtSignal

import dlgo.game_rules_implementation.Player
import dlgo.game_rules_implementation.Point


class GoBoardController(QtWidgets.QGraphicsObject):
    clicked = pyqtSignal(object)

    def __init__(self, board_size):
        super().__init__()
        self.game = None
        self.board_size = 9

        if self.board_size == 9:
            self.margin = 56
        elif self.board_size == 13:
            self.margin = 48
        else:
            self.margin = 47

        self.view_size = 850  # Dimensiunea zonei de vizualizare grafică
        self.cell_size = None
        self.last_move = None
        self.update_cell_size()

    def set_last_move(self, move):
        # Metodă nouă pentru setarea ultimei mutări
        self.last_move = move
        self.update()

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.view_size, self.view_size)

    def update_cell_size(self):
        self.cell_size = round((self.view_size - 2 * self.margin) / (self.board_size - 1))

    def paint(self, painter, option, widget):
        start = self.margin
        end = self.view_size - self.margin

        # Deseneaza liniile grilei
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
                                     end + self.margin + 10), cols[i])

            # Coordonatele din stânga și din dreapta
            # Centrare pe linie verticală
            painter.drawText(QPointF(0, start + i * self.cell_size + painter.fontMetrics().ascent() / 2),
                             str(self.board_size - i))
            painter.drawText(QPointF(end + self.margin,
                                     start + i * self.cell_size + painter.fontMetrics().ascent() / 2),
                             str(self.board_size - i))

        # Desenează intersecțiile principale (Hoshi) pentru o tablă de 9x9
        if self.board_size == 9:
            hoshi_positions = [(3, 3), (3, 7), (7, 3), (7, 7), (5, 5)]
            for pos in hoshi_positions:
                self.draw_hoshi(painter, *pos)

        if self.game is not None:
            board = self.game.board
            for row in range(self.board_size):
                for col in range(self.board_size):
                    stone = board.get(dlgo.game_rules_implementation.Point.Point(row + 1, col + 1))
                    if stone is not None:
                        self.draw_stone(painter, row, col, stone)
        if self.last_move:
            row, col = self.last_move
            self.draw_last_move_marker(painter, row, col)

    def draw_last_move_marker(self, painter, row, col):
        center = QPointF(self.margin + (col - 1) * self.cell_size, self.margin + (row - 1) * self.cell_size)
        radius = self.cell_size * 0.3

        # Setează penița pentru a desena conturul cercului
        pen = QtGui.QPen(QtGui.QColor("grey"))  # Culoare gri pentru contur
        pen.setWidth(2)  # Grosimea liniei; ajustați după preferințe
        painter.setPen(pen)

        # Setează pensula ca fiind transparentă pentru a nu umple cercul
        painter.setBrush(QtCore.Qt.NoBrush)

        # Desenează cercul gol
        painter.drawEllipse(center, radius, radius)

    def draw_hoshi(self, painter, row, col):
        # Calculează centrul și raza pentru hoshi
        row -= 1
        col -= 1
        center_x = self.margin + col * self.cell_size
        center_y = self.margin + row * self.cell_size
        radius = self.cell_size * 0.05  # Raza poate fi ajustată în funcție de preferințe

        painter.setBrush(QtGui.QBrush(QtCore.Qt.black))
        painter.drawEllipse(QtCore.QPointF(center_x, center_y), radius, radius)

    def draw_stone(self, painter, row, col, stone):
        # Calculul centrului și razei pentru pietre
        center_x = self.margin + col * self.cell_size
        center_y = self.margin + row * self.cell_size
        radius = round(self.cell_size // 2)
        color = QtCore.Qt.black if stone == dlgo.game_rules_implementation.Player.Player.black else QtCore.Qt.white
        painter.setBrush(QtGui.QBrush(color))
        painter.drawEllipse(QtCore.QPointF(center_x, center_y), radius, radius)

    def mousePressEvent(self, event):
        # Calculează coordonatele intersecției
        click_pos = event.pos()
        closest_row, closest_col = self.get_closest_intersection(click_pos)

        if closest_row is not None and closest_col is not None:
            self.clicked.emit((closest_row, closest_col))

    def get_closest_intersection(self, click_pos):
        closest_row = closest_col = None
        min_distance = float("inf")  # Inițializează cu o distanță foarte mare

        for row in range(self.board_size):
            for col in range(self.board_size):
                intersection_x = self.margin + col * self.cell_size
                intersection_y = self.margin + row * self.cell_size

                distance = (click_pos.x() - intersection_x) ** 2 + (
                        click_pos.y() - intersection_y
                ) ** 2

                if distance < min_distance:
                    min_distance = distance
                    closest_row = row
                    closest_col = col

        # Verifică dacă distanța este într-un anumit prag (de exemplu, jumătate din dimensiunea celulei)
        if min_distance <= (self.cell_size / 2) ** 2:
            return closest_row + 1, closest_col + 1  # Returnează coordonatele 1-indexate
        else:
            return None, None

    def update_game(self, game):
        self.game = game
        self.update()
