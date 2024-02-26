from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsSimpleTextItem, \
    QGraphicsRectItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtCore

from dlgo import gotypes


class MoveItem(QGraphicsEllipseItem):
    def __init__(self, move_number, player_color, parent=None):
        super().__init__(parent)
        radius = 20
        self.setRect(-radius, -radius, 2*radius, 2*radius)
        self.setBrush(QBrush(player_color))

        # Adaugă numărul mutării
        text_item = QGraphicsSimpleTextItem(str(move_number), self)

        text_color = Qt.white if player_color == Qt.black else Qt.black
        text_item.setBrush(QBrush(text_color))
        text_item.setPos(-radius/2, -radius/2)  # Centrare text


class LastMoveMarker(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRect(-10, -10, 20, 20)  # Dimensiunea markerului
        self.setBrush(Qt.red)
        self.setPen(QPen(Qt.NoPen))  # Fără contur


class GameTreeBoard(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.last_move_marker = None
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.init_board()

    def init_board(self):
        self.setSceneRect(self.scene.itemsBoundingRect())  # Ajustează dimensiunea scenei

    def add_move_to_game_tree(self, move_number, player):
        # Determinați culoarea jucătorului
        color = Qt.black if player == gotypes.Player.black else Qt.white
        move_item = MoveItem(move_number, color)

        x_position = move_number * 50  # Ajustați spațiul după preferințe
        move_item.setPos(x_position, 0)  # Setează poziția orizontală
    
        # Adăugați elementul în scena GameTreeBoard
        self.scene.addItem(move_item)
    
        # Actualizează markerul pentru ultima mutare
        if hasattr(self, 'last_move_marker'):
            self.scene.removeItem(self.last_move_marker)
        self.last_move_marker = LastMoveMarker()
        self.last_move_marker.setPos(x_position, 0)
        self.scene.addItem(self.last_move_marker)
    
        # # Ajustați vizualizarea pentru a arăta noua mutare
        # self.fitInView(self.scene.itemsBoundingRect(), QtCore.KeepAspectRatio)