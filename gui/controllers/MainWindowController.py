import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap

from dlgo import goboards_slow, gotypes, agent
from dlgo.agent import naive
from gui.generated_files.MainWindow import Ui_MainWindow
from gui.section_controllers.GoBoardController import GoBoardController


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.bots = None
        self.timer = None
        self.game = None
        self.board = None
        self.scene = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.board_size = 9
        self.init_GoBoard()

        pixmapW = QPixmap("../resources/TigerW.jpg")
        self.ui.label_IconW.setPixmap(pixmapW)
        self.ui.label_IconW.setScaledContents(True)

        pixmapB = QPixmap("../resources/TigerB.jpg")
        self.ui.label_IconB.setPixmap(pixmapB)
        self.ui.label_IconB.setScaledContents(True)

    def init_GoBoard(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.board = GoBoardController(self.board_size)
        self.scene.addItem(self.board)
        self.scene.setSceneRect(0, 0, 880, 880)  # Updated to match GoBoardController's boundingRect dimensions
        self.ui.graphicsView_GoBoard.setScene(self.scene)
        self.ui.graphicsView_GoBoard.setViewportMargins(0, 0, 0, 0)
        self.ui.graphicsView_GoBoard.centerOn(450, 450)

    def start_bot_game(self):
        self.game = goboards_slow.GameState.new_game(self.board_size)
        self.bots = {
            gotypes.Player.black: agent.naive.RandomBot(),
            gotypes.Player.white: agent.naive.RandomBot(),
        }
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.step_bot_game)
        self.timer.start(300)

    def step_bot_game(self):
        if not self.game.is_over():
            bot_move = self.bots[self.game.next_player].select_move(self.game)
            self.game = self.game.apply_move(bot_move)
            self.board.update_game(self.game)

if __name__ == "__main__":
    os.environ["QT_SCALE_FACTOR"] = "1.5"   # Schimbați acesta la factorul de scalare dorit
    app = QtWidgets.QApplication([])
    ui = MainWindowController()
    ui.showMaximized()
    ui.start_bot_game()
    app.exec_()
