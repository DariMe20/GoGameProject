from datetime import datetime

from PyQt5 import QtWidgets, QtCore

from dlgo.game_rules_implementation.Move import Move, Point
from dlgo.game_rules_implementation.Player import Player
from dlgo.game_rules_implementation.goboard import GameState


class PvBController(QtWidgets.QWidget):
    def __init__(self, GoWin, bot):
        super().__init__()

        self.current_bot = None
        self.current_player = None
        self.GOwin = GoWin
        self.GOwin.ui.label.setText("Player VS BOT")
        self.GOwin.ui.spinBox_numberOfSimulations.hide()
        self.GOwin.ui.label_middleBoard.hide()
        self.GOwin.ui.pushButton_PlayStop.hide()
        self.GOwin.ui.pushButton_EndSimulations.hide()
        self.GOwin.ui.label_2.hide()
        self.GOwin.ui.horizontalSlider.hide()
        # INITIALIZERS
        self.board_size = 9
        self.game = None
        self.bot = bot
        self.is_player_turn = True
        self.board = self.GOwin.board
        self.player_color = self.GOwin.player_color
        self.player_pass = False
        self.bot_pass = False
        self.moves_list = []  # List to store moves
        self.timer = QtCore.QTimer()
        self.GOwin.init_GoBoard()

        self.GOwin.ui.pushButton_StartGame.clicked.connect(self.start_player_game)
        self.GOwin.ui.pushButton_Pass.clicked.connect(self.pass_move)
        self.GOwin.ui.pushButton_Resign.clicked.connect(self.resign_move)
        self.GOwin.ui.pushButton_SaveGame.clicked.connect(self.on_save_sgf)

    def start_player_game(self):
        try:
            self.GOwin.ui.widget_gameStarter.hide()
            self.game = GameState.new_game(self.board_size)
            # Setează culoarea jucătorului și a botului
            if self.player_color == 0:
                self.is_player_turn = True  # Jucătorul începe dacă este negru
                self.current_player = Player.black
                self.current_bot = Player.white
            else:
                self.is_player_turn = False  # Botul începe dacă jucătorul este alb
                self.timer.singleShot(1000, self.agent_move)  # Întârziere pentru a începe jocul cu botul
                self.current_bot = Player.black
                self.current_player = Player.white

            self.board.clicked.connect(self.player_move_against_bot)
        except Exception as e:
            print(f"An error occurred in start player_game: {e}")

    def player_move_against_bot(self, point):
        try:
            if self.is_player_turn and not self.game.is_over():
                row, col = point  # Despachetarea tuplei
                move = Move.play(Point(row, col))
                if self.game.is_valid_move(move):
                    self.GOwin.view_move(self.game, move, self.current_player)
                    self.GOwin.emphasise_player_turn(self.current_player)
                    self.game = self.game.apply_move(move)
                    self.board.set_last_move(move.point)
                    self.moves_list.append((self.current_player, point))  # Store move
                    self.board.update_game(self.game)
                    self.is_player_turn = False
                    self.timer.singleShot(1000, self.agent_move)
                    self.player_pass = False
            self.GOwin.ui.lineEdit_BlackCaptures.setText(str(self.game.white_prisoners) + " Prisoners")
            self.GOwin.ui.lineEdit_WhiteCaptures.setText(str(self.game.black_prisoners) + " Prisoners")
        except Exception as e:
            print(f"An error occurred in player_move: {e}")

    def agent_move(self):
        if not self.game.is_over() and not self.is_player_turn:
            bot_move = self.bot.select_move(self.game)
            if bot_move.is_play:
                self.GOwin.view_move(self.game, bot_move, self.current_bot)
                self.GOwin.emphasise_player_turn(self.current_bot)
                self.game = self.game.apply_move(bot_move)
                self.board.set_last_move(bot_move.point)
                self.moves_list.append((self.current_bot, (bot_move.point.row, bot_move.point.col)))  # Store move
                self.board.update_game(self.game)
                self.bot_pass = False
            elif bot_move.is_pass:
                self.bot_pass = True
                self.GOwin.ui.label.setText(f"{self.current_bot} passed")
                if self.bot_pass is True and self.player_pass is True:
                    self.finalize_game()
                else:
                    self.is_player_turn = True
                    self.bot_pass = False

            elif bot_move.is_resign:
                print("Bot resigned")
                self.finalize_game(resigned=True)
            self.is_player_turn = True
        self.GOwin.ui.lineEdit_BlackCaptures.setText(str(self.game.white_prisoners) + " Prisoners")
        self.GOwin.ui.lineEdit_WhiteCaptures.setText(str(self.game.black_prisoners) + " Prisoners")

    def pass_move(self):
        try:
            if not self.game.is_over() and self.is_player_turn:
                self.player_pass = True
                self.GOwin.ui.label.setText(f"Player passed")

                self.game = self.game.apply_move(Move.pass_turn())
                self.moves_list.append((self.current_player, None))  # Store pass move

                self.current_player = Player.white if self.current_player == Player.black else Player.black
                self.GOwin.emphasise_player_turn(self.current_bot)
                self.is_player_turn = False
                self.timer.singleShot(1000, self.agent_move)
                if self.bot_pass is True and self.player_pass is True:
                    self.finalize_game()
                self.bot_pass = False
        except Exception as e:
            print(f"An error occurred in pass_move: {e}")

    def resign_move(self):
        self.GOwin.ui.label.setText(f"{self.current_player} resigned")
        self.finalize_game(resigned=True)

    def finalize_game(self, resigned=False):
        if not resigned:
            self.GOwin.evaluate_territory_action(self.game)
        winner = self.game.winner()
        result_message = f"{winner} wins" if not resigned else f"{self.current_bot} wins by resignation"
        self.GOwin.ui.label.setText(result_message)
        self.GOwin.evaluate_territory_action(self.game)
        self.GOwin.ui.widget_gameStarter.show()

    def save_to_sgf(self, filename):
        if not self.moves_list:
            print("No moves to save.")
            return

        sgf_content = "(;GM[1]FF[4]SZ[{}]CA[UTF-8]".format(self.board_size)
        sgf_content += "GN[Example Game]DT[{}]".format(datetime.now().strftime("%Y-%m-%d"))

        for player, point in self.moves_list:
            move_str = "B" if player == Player.black else "W"
            if point is not None:
                # SGF coordinates start with 'a' and are reversed vertically
                sgf_col = chr(point[1] - 1 + ord('a'))
                sgf_row = chr(self.board_size - point[0] + ord('a'))
                move_str += "[{}{}]".format(sgf_col, sgf_row)
            else:
                move_str += "[]"
            sgf_content += ";" + move_str

        sgf_content += ")"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sgf_content)

        print(f"Game saved to {filename}")

    def on_save_sgf(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save SGF", "", "SGF Files (*.sgf);;All Files (*)",
                                                            options=options)
        if filename:
            self.save_to_sgf(filename)
