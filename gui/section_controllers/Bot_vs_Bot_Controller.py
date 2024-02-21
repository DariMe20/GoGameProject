import h5py
from PyQt5 import QtWidgets, QtCore
from keras.models import load_model

from dlgo.agent.policy_agent import PolicyAgent
from dlgo import gotypes, goboard
from dlgo.encoders.simple import SimpleEncoder
from dlgo.gotypes import Player


class BvBController(QtWidgets.QWidget):
    def __init__(self, GoWin):
        super().__init__()

        self.completed_simulations = 0
        self.total_simulations = 1
        self.white_pass = False
        self.black_pass = False

        self.black_wins = 0
        self.white_wins = 0

        self.GOwin = GoWin
        self.GOwin.ui.label.setText("BOT VS BOT - Set number of simulations and press Start!")
        
        # INITIALIZERS
        self.board_size = self.GOwin.board_size
        self.game = None
        self.bot_black = None
        self.bot_white = None
        self.board = self.GOwin.board
        self.count_pass = 0
        self.timer = QtCore.QTimer()
        self.GOwin.init_GoBoard()
        self.game_over = False
        self.start = 1

        self.GOwin.ui.widget_4.hide()
        self.GOwin.ui.widget_5.hide()

        # BUTTON CONNECTIONS
        self.GOwin.ui.pushButton_StartGame.clicked.connect(self.start_bot_game)
        self.GOwin.ui.pushButton_EndSimulations.clicked.connect(self.end_state)
        self.GOwin.ui.pushButton_PlayStop.clicked.connect(self.toggle_play_stop)

        # SLIDER SETTINGS
        self.GOwin.ui.horizontalSlider.setMaximum(3500)
        self.GOwin.ui.horizontalSlider.setMinimum(100)
        self.GOwin.ui.horizontalSlider.setTickInterval(500)
        self.GOwin.ui.horizontalSlider.setValue(500)
        self.GOwin.ui.horizontalSlider.setInvertedAppearance(True)
        self.GOwin.ui.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.GOwin.ui.horizontalSlider.valueChanged.connect(self.update_timer_interval)
        self.update_timer_interval(250)

        # model_path_policy = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient2.h5'
        # model_path_predict = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model2.h5'

        model_path1 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient2.h5'
        self.model_p1 = load_model(model_path1)

        model_path2 = 'C:\\Users\\MED6CLJ\\Desktop\\FSEGA_IE\\Licenta\\GoGameProject\\dlgo\\keras_networks\\model_gradient4.h5'
        self.model_p2 = load_model(model_path2)

        # self.model_policy = load_policy_agent(model_path_policy)
        # self.model_predict = load_model(model_path_predict)
        self.encoder = SimpleEncoder(board_size=(self.board_size, self.board_size))

    #SLIDER METHODS
    def update_timer_interval(self, value):
        # Aici puteți actualiza intervalele timer-ului
        self.timer.setInterval(value)
        self.update_slider_labels(value)

    def update_slider_labels(self, value):
        # Aici puteți actualiza etichetele dacă aveți nevoie
        self.GOwin.ui.label_2.setText(f"Playing speed: {value} ms")
    def toggle_play_stop(self):
        if self.start == 1:
            self.timer.stop()
            self.start = 0
            self.GOwin.ui.pushButton_PlayStop.setText('Play Game')
        else:
            self.start = 1
            self.timer.start()
            self.GOwin.ui.pushButton_PlayStop.setText('Stop Game')
    def start_bot_game(self):
        try:
            self.total_simulations = self.GOwin.ui.spinBox_numberOfSimulations.value()
            self.completed_simulations = 0
            self.GOwin.ui.widget_gameStarter.hide()
            self.run_simulation()

        except Exception as e:
            print("Error in start bot game: ", e)

    def run_simulation(self):
        if self.GOwin.reset == 1 or self.completed_simulations >= self.total_simulations:
            self.game_over = True
            return
        self.game = goboard.GameState.new_game(self.board_size)
        self.bot_black = PolicyAgent(self.model_p1, self.encoder)
        self.bot_white = PolicyAgent(self.model_p2, self.encoder)
        self.game_over = False
        # self.bot_black = load_policy_agent(h5py.File(self.model_path_policy))
        # self.bot_white = DeepLearningAgent(self.model_predict, self.encoder)
        self.GOwin.ui.verticalWidget.setStyleSheet('#verticalWidget{border:1px solid blue;}')
        self.GOwin.ui.verticalWidget_2.setStyleSheet("#verticalWidget_2{border:none}")
        self.timer = QtCore.QTimer()

        self.timer.timeout.connect(self.step_bot_game)
        self.timer.start()

    def step_bot_game(self):
        try:
            if self.GOwin.reset == 1 or self.game_over:
                return

            current_player = self.game.next_player
            bot_agent = self.bot_black if current_player == gotypes.Player.black else self.bot_white

            self.GOwin.ui.label_FinalResults.setText(f"Showing probs for agent: {current_player}")

            bot_probs = self.bot_black if current_player == gotypes.Player.white else self.bot_white
            move_probs_html = bot_probs.generate_gui_formatted_probs(self.game)
            self.GOwin.ui.textEdit_Probs.setHtml(move_probs_html)
            bot_move = bot_agent.select_move(self.game)

            # Aplică mutarea și actualizează starea jocului
            self.game = self.game.apply_move(bot_move)
            self.update_prisoners()

            # Verifică pentru două pasări consecutive
            if self.game.is_over():
                self.finalize_game()
                return

            if not bot_move.is_pass:
                self.GOwin.view_move(self.game, bot_move, current_player)
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
        winner = self.game.winner()
        if winner == Player.black:
            self.black_wins += 1
        else:
            self.white_wins += 1
        self.completed_simulations += 1

        if self.completed_simulations < self.total_simulations:
            self.GOwin.ui.label_game.setText(f"Playing Game {self.completed_simulations + 1}\n"
                                             f"{self.completed_simulations} SIMULATIONS COMPLETED: "
                                             f"Black wins: {self.black_wins} \ {self.completed_simulations}  "
                                             f"White wins: {self.white_wins} \ {self.completed_simulations}")
            self.run_simulation()
        else:
            self.end_state()

    def end_state(self):
        self.game_over = True
        self.timer.stop()
        if self.black_wins > self.white_wins:
            self.GOwin.ui.label_game.setText(f"AFTER {self.completed_simulations} SIMULATIONS COMPLETED: "
                                             f"Black IS STRONGER with: {self.black_wins} \ {self.completed_simulations} wins"
                                             )
        elif self.black_wins < self.white_wins:
            self.GOwin.ui.label_game.setText(f"AFTER {self.completed_simulations} SIMULATIONS COMPLETED: "
                                             f"White IS STRONGER with: {self.white_wins} \ {self.completed_simulations} wins"
                                             )
        else:
            self.GOwin.ui.label_game.setText(f"AFTER {self.completed_simulations} SIMULATIONS COMPLETED: "
                                             f"White and Black are equally strong!")

        self.GOwin.ui.widget_gameStarter.show()
        self.black_wins = 0
        self.white_wins = 0
        self.completed_simulations = 0

    def update_prisoners(self):
        self.GOwin.ui.lineEdit_BlackCaptures.setText(str(self.game.white_prisoners) + " Prisoners")
        self.GOwin.ui.lineEdit_WhiteCaptures.setText(str(self.game.black_prisoners) + " Prisoners")


