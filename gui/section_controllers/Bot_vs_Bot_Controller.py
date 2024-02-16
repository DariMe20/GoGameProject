from PyQt5 import QtWidgets, QtCore
from keras.models import load_model

from dlgo.agent.policy_agent import PolicyAgent
from dlgo.agent.predict import DeepLearningAgent
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo import gotypes, goboard
from dlgo.encoders.simple import SimpleEncoder


class BvBController(QtWidgets.QWidget):
    def __init__(self, GoWin):
        super().__init__()

        self.white_pass = False
        self.black_pass = False
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
        self.game_over = False

        self.GOwin.ui.pushButton_StartGame.clicked.connect(self.start_bot_game)

        model_path_policy = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\black_agent_model6.h5'
        model_path_predict = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model2.h5'

        self.model_policy = load_model(model_path_policy)
        self.model_predict = load_model(model_path_predict)
        self.encoder = SimpleEncoder(board_size=(self.board_size, self.board_size))



    def start_bot_game(self):
        if self.GOwin.reset == 1:
            return

        self.game = goboard.GameState.new_game(self.board_size)
        # self.bot_black = DeepLearningAgent(self.model, self.encoder)
        # self.bot_white = DeepLearningAgent(self.model, self.encoder)
        self.bot_black = PolicyAgent(self.model_policy, self.encoder, gotypes.Player.black)
        self.bot_white = DeepLearningAgent(self.model_predict, self.encoder)
        self.GOwin.ui.verticalWidget.setStyleSheet('#verticalWidget{border:1px solid blue;}')
        self.GOwin.ui.verticalWidget_2.setStyleSheet("#verticalWidget_2{border:none}")
        self.timer = QtCore.QTimer()

        self.timer.timeout.connect(self.step_bot_game)
        self.timer.start(500)


    def step_bot_game(self):
        try:
            if self.GOwin.reset == 1 or self.game_over:
                return

            current_player = self.game.next_player
            bot_agent = self.bot_black if current_player == gotypes.Player.black else self.bot_white

            bot_move = bot_agent.select_move(self.game)

            # Aplică mutarea și actualizează starea jocului
            self.game = self.game.apply_move(bot_move)
            self.update_prisoners()

            # Verifică pentru două pasări consecutive
            if self.game.last_move.is_pass and self.game.previous_state.last_move.is_pass:
                self.finalize_game()
                return

            if not bot_move.is_pass:
                self.GOwin.view_move(bot_move, current_player)
                self.GOwin.emphasise_player_turn(current_player.other)
            else:
                self.GOwin.ui.label.setText(f"{current_player} passed")

            # Actualizează tabla de joc GUI
            self.board.update_game(self.game)

            if bot_move.is_resign:
                self.GOwin.ui.label.setText(f"{current_player} resigned")
                self.game_over = True
                self.timer.stop()
        except Exception as e:
            print("Error in step_bot_game: ", e)

    def finalize_game(self):
        self.GOwin.evaluate_territory_action(self.game)
        self.game_over = True
        self.timer.stop()


    def update_prisoners(self):
        self.GOwin.ui.lineEdit_BlackCaptures.setText(str(self.game.white_prisoners) + " Prisoners")
        self.GOwin.ui.lineEdit_WhiteCaptures.setText(str(self.game.black_prisoners) + " Prisoners")


