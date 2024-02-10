from PyQt5 import QtWidgets, QtCore
from tensorflow.keras.models import load_model
from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo import gotypes, goboard


class CreateSGFController(QtWidgets.QWidget):
    def __init__(self, GoWin):
        super().__init__()

        self.current_player = None
        self.GOwin = GoWin
        self.GOwin.ui.label.setText("Create SGF YAAY")

        # INITIALIZERS
        self.board_size = self.GOwin.board_size
        self.game = None
        self.bot_black = None
        self.bot_white = None
        self.board = self.GOwin.board
        self.count_pass = 0
        self.timer = QtCore.QTimer
        self.GOwin.init_GoBoard()
        self.create_sgf_game()

        self.GOwin.ui.pushButton_StartGame.hide()
        self.GOwin.ui.verticalWidget.setStyleSheet('#verticalWidget{border:1px solid blue;}')
        self.GOwin.ui.verticalWidget_2.setStyleSheet("#verticalWidget_2{border:none}")

    def create_sgf_game(self):
        self.game = goboard.GameState.new_game(self.board_size)
        self.current_player = gotypes.Player.black
        self.board.clicked.connect(self.player_move)

    def player_move(self, point):
        if not self.game.is_over():
            self.GOwin.emphasise_player_turn(self.current_player)

            row, col = point  # Despachetarea tuplei
            move = goboard.Move.play(gotypes.Point(row, col))
            if self.game.is_valid_move(move) and self.game.next_player == self.current_player:
                self.game = self.game.apply_move(move)
                self.board.update_game(self.game)

                self.GOwin.view_move(move, self.current_player)

                # Alternează între jucătorul negru și alb
                self.current_player = gotypes.Player.white if self.current_player == gotypes.Player.black else gotypes.Player.black
