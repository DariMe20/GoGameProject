from PyQt5 import QtWidgets, QtCore

import dlgo.game_rules_implementation.Move
import dlgo.game_rules_implementation.Player
import dlgo.game_rules_implementation.Point
from dlgo.game_rules_implementation import goboard
from gui.section_controllers.GameTreeController import GameTreeBoard


class CreateSGFController(QtWidgets.QWidget):
    def __init__(self, GoWin):
        super().__init__()

        self.gameTree = None
        self.scene = None
        self.current_player = None
        self.GOwin = GoWin
        self.GOwin.ui.label.setText("Create SGF YAAY")

        # PAGE EDITORS AND HIDERS
        self.GOwin.ui.widget_gameStarter.hide()
        self.GOwin.ui.pushButton_best5Moves.hide()
        self.GOwin.ui.pushButton_PlayStop.hide()
        self.GOwin.ui.pushButton_EndSimulations.hide()
        self.GOwin.ui.label_2.hide()
        self.GOwin.ui.horizontalSlider.hide()
        self.GOwin.ui.stackedWidget_Probs_TreeView.setCurrentIndex(1)

        # INITIALIZERS
        self.board_size = self.GOwin.board_size
        self.game = None
        self.bot_black = None
        self.bot_white = None
        self.board = self.GOwin.board
        self.count_pass = 0
        self.timer = QtCore.QTimer
        self.GOwin.init_GoBoard()

        self.GOwin.ui.pushButton_StartGame.hide()
        self.GOwin.ui.verticalWidget.setStyleSheet('#verticalWidget{border:1px solid gray;}')
        self.GOwin.ui.verticalWidget_2.setStyleSheet("#verticalWidget_2{border:none}")

        # TREE LIST
        self.moves_list = []
        self.init_gameTree()
        self.create_sgf_game()

    def create_sgf_game(self):
        self.game = goboard.GameState.new_game(self.board_size)
        self.current_player = dlgo.game_rules_implementation.Player.Player.black
        self.GOwin.ui.lineEdit_BlackCaptures.setText(str(self.game.white_prisoners) + " Prisoners")
        self.GOwin.ui.lineEdit_WhiteCaptures.setText(str(self.game.black_prisoners) + " Prisoners")
        self.board.clicked.connect(self.player_move)

    def init_gameTree(self):
        if not self.scene and not self.gameTree:
            self.scene = QtWidgets.QGraphicsScene()
            self.gameTree = GameTreeBoard()
            self.GOwin.ui.graphicsView_GameTree.setScene(self.gameTree.scene)
            self.moves_list.clear()

    def player_move(self, point):
        try:
            if not self.game.is_over():

                row, col = point  # Despachetarea tuplei
                move = dlgo.game_rules_implementation.Move.Move.play(
                    dlgo.game_rules_implementation.Point.Point(row, col))
                if self.game.is_valid_move(move) and self.game.next_player == self.current_player:
                    self.GOwin.emphasise_player_turn(self.current_player)
                    self.game = self.game.apply_move(move)
                    self.board.set_last_move(point)
                    self.board.update_game(self.game)

                    self.GOwin.view_move(self.game, move, self.current_player)
                    #
                    # Adaugă mutarea în listă și în QTreeView
                    move_number = self.game.move_number
                    self.gameTree.add_move_to_game_tree(move_number, self.current_player)
                    self.moves_list.append((self.current_player, point))

                    # Alternează între jucătorul negru și alb
                    self.current_player = dlgo.game_rules_implementation.Player.Player.white if self.current_player == dlgo.game_rules_implementation.Player.Player.black else dlgo.game_rules_implementation.Player.Player.black

                self.GOwin.ui.lineEdit_BlackCaptures.setText(str(self.game.white_prisoners) + " Prisoners")
                self.GOwin.ui.lineEdit_WhiteCaptures.setText(str(self.game.black_prisoners) + " Prisoners")
        except Exception as e:
            print(f"Exception in player_move in CreateSGFController: {e}")
