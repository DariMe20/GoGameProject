import os
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QFont

from dlgo import goboards_slow, gotypes, agent
from dlgo.agent import naive
from gui.generated_files.MainWindow import Ui_MainWindow
from gui.section_controllers.GoBoardController import GoBoardController


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.bot = None
        self.is_player_turn = True
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

        # BUTTON CONNECTIONS
        self.ui.pushButton_BotVBot.clicked.connect(self.start_bot_game)
        self.ui.pushButton_PlayBot.clicked.connect(self.start_player_game)

    def draw_coordinates(self):
        pass

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

    def start_player_game(self):
        try:
            self.game = goboards_slow.GameState.new_game(self.board_size)
            self.bot = agent.naive.RandomBot()  # Inițializează botul
            self.is_player_turn = True  # Setează rândul jucătorului

            # Conectează un eveniment de clic pe tablă la o metodă care gestionează mișcările jucătorului
            self.board.clicked.connect(self.player_move)
        except Exception as e:
            print(f"An error occurend: {e}")

    def player_move(self, point):
        try:
            if self.is_player_turn and not self.game.is_over():
                row, col = point  # Despachetarea tuplei
                move = goboards_slow.Move.play(gotypes.Point(row, col))
                if self.game.is_valid_move(move):
                    self.game = self.game.apply_move(move)
                    self.board.update_game(self.game)
                    self.is_player_turn = False
                    self.step_bot_game_player()  # Permite botului să facă o mișcare
        except Exception as e:
            print(f"An error occurend: {e}")

    def step_bot_game_player(self):
        try:
            if not self.game.is_over() and not self.is_player_turn:
                bot_move = self.bot.select_move(self.game)
                self.game = self.game.apply_move(bot_move)
                self.board.update_game(self.game)
                self.is_player_turn = True
        except Exception as e:
            print(f"An error occurend: {e}")

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
    ui.showMaximized()
    # Inchidere aplicatie
    sys.exit(app.exec_())
