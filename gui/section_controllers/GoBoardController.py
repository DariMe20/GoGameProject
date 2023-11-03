from PyQt5 import QtWidgets, QtCore, QtGui


class GoBoardController(QtWidgets.QGraphicsItem):
    def __init__(self, board_size):
        super().__init__()
        self.board_size = board_size

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 900, 900)

    def paint(self, painter, option, widget):
        start = 15
        end = 860
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
            painter.drawText(start + i * cell_size - 5, start - 13, cols[i])
            painter.drawText(start + i * cell_size - 5, end + 25, cols[i])

            # Coordonatele din stânga și din dreapta
            painter.drawText(start - 25, start + i * cell_size + 5, str(self.board_size - i))
            painter.drawText(end + 15, start + i * cell_size + 5, str(self.board_size - i))
