from PyQt5 import QtWidgets, QtCore
from tensorflow.keras.models import load_model
from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo import gotypes, goboard


class BvBController(QtWidgets.QWidget):
    def __init__(self, GoWin):
        super().__init__()

        self.GOwin = GoWin
        self.GOwin.ui.label.setText("BOT VS BOT YAAY")
        
        # INITIALIZERS
        self.board_size = self.GOwin.board_size
        self.game = None
        self.bot_black = None
        self.bot_white = None
        self.board = self.GOwin.board
        self.count_pass = 0
        self.timer = QtCore.QTimer
        self.GOwin.init_GoBoard()

        self.GOwin.ui.pushButton_StartGame.clicked.connect(self.start_bot_game)

        model_path = 'C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\model2.h5'

        self.model = load_model(model_path)
        self.encoder = OnePlaneEncoder(board_size=(self.board_size, self.board_size))
        self.deep_learning_agent = DeepLearningAgent(self.model, self.encoder)

    def start_bot_game(self):
        if self.GOwin.reset == 1:
            return

        self.game = goboard.GameState.new_game(self.board_size)
        self.bot_black = DeepLearningAgent(self.model, self.encoder)
        self.bot_white = DeepLearningAgent(self.model, self.encoder)
        self.GOwin.ui.verticalWidget.setStyleSheet('#verticalWidget{border:1px solid blue;}')
        self.GOwin.ui.verticalWidget_2.setStyleSheet("#verticalWidget_2{border:none}")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.step_bot_game)
        self.timer.start(2000)
        if self.count_pass == 2:
            self.GOwin.ui.label.setText("BOTH BOTS PASSED. GAME IS OVER")
            return

    def step_bot_game(self):
        try:
            if self.GOwin.reset == 1:
                return

            if not self.game.is_over():
                current_player = self.game.next_player
                bot_move = (
                    self.bot_black
                    if current_player == gotypes.Player.black
                    else self.bot_white
                ).select_move(self.game)

                self.GOwin.emphasise_player_turn(current_player)

                if bot_move.is_play:
                    self.game = self.game.apply_move(bot_move)
                    self.board.update_game(self.game)

                    self.GOwin.view_move(bot_move, current_player)

                elif bot_move.is_pass:
                    if current_player == gotypes.Player.black:
                        self.GOwin.ui.label.setText("Black passed")
                    else:
                        self.GOwin.ui.label.setText("White passed")
                    self.count_pass += 1

                elif bot_move.is_resign:
                    if current_player == gotypes.Player.black:
                        self.GOwin.ui.label.setText("Black resigned")
                    else:
                        self.GOwin.ui.label.setText("White resigned")

        except Exception as e:
            print(f"An error occurend in bot_v_bot game: {e}")