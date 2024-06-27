from PyQt5 import QtWidgets, QtCore

from dlgo.game_rules_implementation import goboard
from dlgo.game_rules_implementation.Player import Player


class BvBController(QtWidgets.QWidget):
    def __init__(self, GoWin, bot_black, bot_white):
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
        self.bot_black = bot_black
        self.bot_white = bot_white
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
        self.GOwin.ui.pushButton_SaveGame.hide()

        # SLIDER SETTINGS
        self.default_Value = 1000
        self.GOwin.ui.horizontalSlider.setMaximum(2500)
        self.GOwin.ui.horizontalSlider.setMinimum(200)
        self.GOwin.ui.horizontalSlider.setTickInterval(50)
        self.update_slider_labels(self.default_Value)
        self.timer.setInterval(self.default_Value)
        self.GOwin.ui.horizontalSlider.setInvertedAppearance(True)
        self.GOwin.ui.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.GOwin.ui.horizontalSlider.valueChanged.connect(self.update_timer_interval)

    # SLIDER METHODS
    def update_timer_interval(self, value):
        self.default_Value = value
        self.timer.setInterval(value)
        self.update_slider_labels(value)

    def update_slider_labels(self, value):
        self.GOwin.ui.label_2.setText(f"Playing speed: {value} ms")

    # TOGGLER
    def toggle_play_stop(self):
        if self.start == 1:
            self.timer.stop()
            self.start = 0
            self.GOwin.ui.pushButton_PlayStop.setText('Play Game')
        else:
            self.start = 1
            self.timer.start()
            self.GOwin.ui.pushButton_PlayStop.setText('Stop Game')

    # PLAY METHODS
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
        self.game_over = False

        self.GOwin.ui.verticalWidget.setStyleSheet('#verticalWidget{border:1px solid grey;}')
        self.GOwin.ui.verticalWidget_2.setStyleSheet("#verticalWidget_2{border:none}")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.step_bot_game)
        self.timer.start(500)

    def step_bot_game(self):
        try:
            if self.GOwin.reset == 1 or self.game_over:
                return

            current_player = self.game.next_player
            bot_agent = self.bot_black if current_player == Player.black else self.bot_white

            self.GOwin.ui.label_FinalResults.setText(f"Showing probs for agent: {current_player}")

            bot_probs = self.bot_black if current_player == Player.white else self.bot_white

            if bot_probs.compute_probs is True:
                move_probs_html = bot_probs.generate_gui_formatted_probs(self.game)
                self.GOwin.ui.textEdit_Probs.setHtml(move_probs_html)
            bot_move = bot_agent.select_move(self.game)

            # Aplică mutarea și actualizează starea jocului
            self.game = self.game.apply_move(bot_move)
            self.board.set_last_move(bot_move.point)
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
