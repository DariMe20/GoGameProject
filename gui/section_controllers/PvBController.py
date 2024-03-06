from PyQt5 import QtWidgets, QtCore
from keras.src.saving.saving_api import load_model

import dlgo.game_rules_implementation.Move
import dlgo.game_rules_implementation.Player
import dlgo.game_rules_implementation.Point
from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.game_rules_implementation import goboard


class PvBController(QtWidgets.QWidget):
    def __init__(self, GoWin):
        super().__init__()

        self.current_bot = None
        self.current_player = None
        self.GOwin = GoWin
        self.GOwin.ui.label.setText("Player VS BOT YAAY")

        # INITIALIZERS
        self.board_size = self.GOwin.board_size
        self.game = None
        self.bot = None
        self.is_player_turn = True
        self.board = self.GOwin.board
        self.player_color = self.GOwin.player_color
        self.count_pass = 0
        self.timer = QtCore.QTimer
        self.GOwin.init_GoBoard()

        self.GOwin.ui.pushButton_StartGame.clicked.connect(self.start_player_game)

        model_path = 'C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\model_PredictionAgent.h5'

        self.model = load_model(model_path)
        self.encoder = OnePlaneEncoder(board_size=(self.board_size, self.board_size))
        self.deep_learning_agent = DeepLearningAgent(self.model, self.encoder)

    def start_player_game(self):
        try:
            self.game = goboard.GameState.new_game(self.board_size)
            # Setează culoarea jucătorului și a botului
            if self.player_color == 0:
                self.is_player_turn = True  # Jucătorul începe dacă este negru
                self.current_player = dlgo.game_rules_implementation.Player.Player.black
                self.current_bot = dlgo.game_rules_implementation.Player.Player.white
            else:
                self.is_player_turn = False  # Botul începe dacă jucătorul este alb
                self.timer.singleShot(1000, self.agent_move)  # Întârziere pentru a începe jocul cu botul
                self.current_bot = dlgo.game_rules_implementation.Player.Player.black
                self.current_player = dlgo.game_rules_implementation.Player.Player.white

            self.bot = DeepLearningAgent(self.model, self.encoder)
            self.board.clicked.connect(self.player_move_against_bot)
        except Exception as e:
            print(f"An error occurred in start player_game: {e}")

    def player_move_against_bot(self, point):
        try:
            if self.is_player_turn and not self.game.is_over():
                row, col = point  # Despachetarea tuplei
                move = dlgo.game_rules_implementation.Move.Move.play(
                    dlgo.game_rules_implementation.Point.Point(row, col))
                if self.game.is_valid_move(move):
                    self.GOwin.view_move(self.game, move, self.current_player)
                    self.GOwin.emphasise_player_turn(self.current_player)
                    self.game = self.game.apply_move(move)
                    self.board.update_game(self.game)
                    self.is_player_turn = False
                    self.timer.singleShot(1000, self.agent_move)
            self.GOwin.ui.lineEdit_BlackCaptures.setText(str(self.game.white_prisoners) + " Prisoners")
            self.GOwin.ui.lineEdit_WhiteCaptures.setText(str(self.game.black_prisoners) + " Prisoners")
        except Exception as e:
            print(f"An error occurend in player_move: {e}")

    def agent_move(self):
        if not self.game.is_over() and not self.is_player_turn:
            bot_move = self.deep_learning_agent.select_move(self.game)
            if bot_move.is_play:
                self.GOwin.view_move(self.game, bot_move, self.current_bot)
                self.GOwin.emphasise_player_turn(self.current_bot)

                self.game = self.game.apply_move(bot_move)
                self.board.update_game(self.game)
            elif bot_move.is_pass:
                print("Bot passed")
            elif bot_move.is_resign:
                print("Bot resigned")
            self.is_player_turn = True
        self.GOwin.ui.lineEdit_BlackCaptures.setText(str(self.game.white_prisoners) + " Prisoners")
        self.GOwin.ui.lineEdit_WhiteCaptures.setText(str(self.game.black_prisoners) + " Prisoners")
