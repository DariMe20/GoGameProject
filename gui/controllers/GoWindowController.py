import os
import sys

import h5py
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QFont
# from tensorflow.keras.models import load_model
# from dlgo.agent.predict import DeepLearningAgent
# from dlgo.encoders.oneplane import OnePlaneEncoder
# from dlgo.kerasutil import load_model_from_hdf5_group
# from MonteCarloTreeSearch.MCTS import MCTSAgent
# from dlgo import gotypes, agent, goboard
from gui.generated_files.MainWindow import Ui_MainWindow
from gui.section_controllers.GoBoardController import GoBoardController


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, nameW, nameB, player_color=0, board_size=9, handicap=0, komi=6.5):
        super().__init__()
        self.current_player = None
        self.bot_black = None
        self.bot_white = None
        self.bot = None
        self.is_player_turn = True
        self.bots = None
        self.game = None
        self.board = None
        self.scene = None
        self.count_pass = 0
        self.timer = QtCore.QTimer

        # INITIALIZATORI
        self.nameW = nameW
        self.nameB = nameB
        self.player_color = player_color
        self.board_size = board_size
        self.handicap = handicap
        self.komi = komi

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_GoBoard()

        pixmapW = QPixmap("../resources/TigerW.jpg")
        self.ui.label_IconW.setPixmap(pixmapW)
        self.ui.label_IconW.setScaledContents(True)

        pixmapB = QPixmap("../resources/TigerB.jpg")
        self.ui.label_IconB.setPixmap(pixmapB)
        self.ui.label_IconB.setScaledContents(True)

        # LINE EDITS
        self.ui.BlackPlayerName.setText(self.nameB)
        self.ui.WhitePlayerName.setText(self.nameW)
        self.ui.label.setText("Empty board. Black to play.")

        # # BUTTON CONNECTIONS
        # self.ui.pushButton_BotVBot.clicked.connect(self.start_bot_game)
        # self.ui.pushButton_PlayBot.clicked.connect(self.start_player_game)
        # self.ui.pushButton_CreateSGF.clicked.connect(self.create_sgf_game)
        #
        # model_path = 'C:\\DARIA\\1.FSEGA\\LICENTA\\GoGameProject\\dlgo\\keras_networks\\model2.h5'
        #
        # self.model = load_model(model_path)
        # self.encoder = OnePlaneEncoder(board_size=(self.board_size, self.board_size))
        # self.deep_learning_agent = DeepLearningAgent(self.model, self.encoder)


    def init_GoBoard(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.board = GoBoardController(self.board_size)
        self.scene.addItem(self.board)
        self.scene.setSceneRect(
            0, 0, 850, 850
        )  # Updated to match GoBoardController's boundingRect dimensions
        self.ui.graphicsView_GoBoard.setScene(self.scene)
        self.ui.graphicsView_GoBoard.setViewportMargins(0, 0, 0, 0)
        self.ui.graphicsView_GoBoard.centerOn(425, 425)

    # def create_sgf_game(self):
    #     self.game = goboard.GameState.new_game(self.board_size)
    #     self.current_player = gotypes.Player.black
    #     self.board.clicked.connect(self.player_move)
    #
    # def player_move(self, point):
    #     if not self.game.is_over():
    #         row, col = point  # Despachetarea tuplei
    #         move = goboard.Move.play(gotypes.Point(row, col))
    #         if self.game.is_valid_move(move) and self.game.next_player == self.current_player:
    #             self.game = self.game.apply_move(move)
    #             self.board.update_game(self.game)
    #             # Alternează între jucătorul negru și alb
    #             self.current_player = gotypes.Player.white if self.current_player == gotypes.Player.black else gotypes.Player.black
    #         else:
    #             print("Mutare invalidă sau nu este rândul jucătorului!")
    #
    # def start_player_game(self):
    #     try:
    #         self.game = goboard.GameState.new_game(self.board_size)
    #         self.bot = DeepLearningAgent(self.model, self.encoder)  # Inițializează botul
    #
    #         # Conectează un eveniment de clic pe tablă la o metodă care gestionează mișcările jucătorului
    #         self.board.clicked.connect(self.player_move_against_bot)
    #     except Exception as e:
    #         print(f"An error occurend in start player_game: {e}")
    #
    # def player_move_against_bot(self, point):
    #     try:
    #         if self.is_player_turn and not self.game.is_over():
    #             row, col = point  # Despachetarea tuplei
    #             move = goboard.Move.play(gotypes.Point(row, col))
    #             if self.game.is_valid_move(move):
    #                 self.game = self.game.apply_move(move)
    #                 self.board.update_game(self.game)
    #                 self.is_player_turn = False
    #                 self.agent_move()
    #     except Exception as e:
    #         print(f"An error occurend in player_move: {e}")
    #
    # def agent_move(self):
    #     if not self.game.is_over() and not self.is_player_turn:
    #         bot_move = self.deep_learning_agent.select_move(self.game)
    #         if bot_move.is_play:
    #             self.game = self.game.apply_move(bot_move)
    #             self.board.update_game(self.game)
    #         elif bot_move.is_pass:
    #             print("Bot passed")
    #         elif bot_move.is_resign:
    #             print("Bot resigned")
    #         self.is_player_turn = True
    #
    # def step_bot_game_player(self):
    #     try:
    #         if not self.game.is_over() and not self.is_player_turn:
    #             bot_move = self.bot.select_moveMCTS(self.game)
    #             self.game = self.game.apply_move(bot_move)
    #             self.board.update_game(self.game)
    #             self.is_player_turn = True
    #     except Exception as e:
    #         print(f"An error occurend in step_bot_game_player: {e}")
    #
    # def start_bot_game(self):
    #     self.game = goboard.GameState.new_game(self.board_size)
    #     self.bot_black = DeepLearningAgent(self.model, self.encoder)
    #     self.bot_white = DeepLearningAgent(self.model, self.encoder)
    #     self.timer = QtCore.QTimer()
    #     self.timer.timeout.connect(self.step_bot_game)
    #     self.timer.start(1000)  # De exemplu, o mutare la fiecare secundă
    #     if self.count_pass == 2:
    #         print("Game is over")
    #         return
    #
    #
    # def step_bot_game(self):
    #     try:
    #         if not self.game.is_over():
    #             current_player = self.game.next_player
    #             bot_move = (
    #                 self.bot_black
    #                 if current_player == gotypes.Player.black
    #                 else self.bot_white
    #             ).select_move(self.game)
    #
    #             if bot_move.is_play:
    #                 self.game = self.game.apply_move(bot_move)
    #                 self.board.update_game(self.game)
    #             elif bot_move.is_pass:
    #                 self.count_pass += 1
    #                 print(f"Bot {current_player} passed")
    #             elif bot_move.is_resign:
    #                 print(f"Bot {current_player} resigned")
    #     except Exception as e:
    #         print(f"An error occurend in bot_v_bot game: {e}")

    @staticmethod
    def adjust_scale_factor():
        temp_app = QtWidgets.QApplication(
            sys.argv
        )  # Instanță temporară pentru a obține informații despre ecran
        screen = temp_app.primaryScreen()
        resolution = screen.size()  # Ia rezolutia ecranului
        scale_factor = "1"  # Factor de scalare default

        high_res_threshold_width = 2560  # threshold latime
        high_res_threshold_height = 1440  # threshold lungime

        # Daca avem o rezolutie a ecranului foarte mare, setam factorul de scalare la 1.5
        if (
                resolution.width() > high_res_threshold_width
                and resolution.height() > high_res_threshold_height
        ):
            scale_factor = "1.5"

        # Setare factor de scalare
        os.environ["QT_SCALE_FACTOR"] = scale_factor
        temp_app.quit()  # Închideți instanța temporară


# Main
if __name__ == "__main__":
    # Ajustez factorul de scalare înainte de a crea QApplication
    MainWindowController.adjust_scale_factor()

    # Generearea instanței reale pentru aplicație
    app = QtWidgets.QApplication(sys.argv)
    # Instantiere obiect
    ui = MainWindowController()
    # Afisare obiect in fereastra deschisa larg
    ui.show()
    # Inchidere aplicatie
    sys.exit(app.exec_())
