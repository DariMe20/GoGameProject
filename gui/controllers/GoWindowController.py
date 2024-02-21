import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from dlgo import gotypes
from dlgo.gotypes import Player, Point
from gui.generated_files.MainWindow import Ui_MainWindow
from gui.section_controllers.Bot_vs_Bot_Controller import BvBController
from gui.section_controllers.CreateSGFController import CreateSGFController
from gui.section_controllers.GoBoardController import GoBoardController
from gui.section_controllers.PvBController import PvBController


class GoWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, nameB, nameW, situation_controller, player_color=3, board_size=9, handicap=0, komi=6.5):
        super().__init__()

        # PAGE CONTROLLERS
        self.PvBController = None
        self.CreateSGFController = None
        self.BvBController = None

        # INITIALIZATORI
        self.reset = 0
        self.board = None
        self.scene = None
        self.nameW = nameW
        self.nameB = nameB
        self.player_color = player_color
        self.board_size = board_size
        self.handicap = handicap
        self.komi = komi
        self.situation_controller = situation_controller

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

        self.redirect_to_situation()

    def redirect_to_situation(self):
        if self.situation_controller == 1:
            self.CreateSGFController = CreateSGFController(self)

        if self.situation_controller == 3:
            self.PvBController = PvBController(self)

        if self.situation_controller == 4:
            self.BvBController = BvBController(self)

    def init_GoBoard(self):
        if not self.scene and not self.board:
            self.scene = QtWidgets.QGraphicsScene()
            self.board = GoBoardController(self.board_size)
            self.scene.addItem(self.board)
            self.scene.setSceneRect(
                0, 0, 850, 850
            )  # Updated to match GoBoardController's boundingRect dimensions
            self.ui.graphicsView_GoBoard.setScene(self.scene)
            self.ui.graphicsView_GoBoard.setViewportMargins(0, 0, 0, 0)
            self.ui.graphicsView_GoBoard.centerOn(425, 425)

    def view_move(self, state, move, current_player):
        go_coord = self.point_to_coord(move.point, self.board_size)
        player_color = "B" if current_player == gotypes.Player.black else "W"
        next_player = "Black" if current_player == gotypes.Player.white else "White"
        self.ui.label.setText(f"Move {state.move_number}: {player_color} - {go_coord}. {next_player} to play.")

    def point_to_coord(self, point, board_size):
        col_names = "ABCDEFGHJKLMNOPQRST"
        row = board_size - point.row + 1
        col = col_names[point.col - 1]
        return f"{col}{row}"

    def emphasise_player_turn(self, current_player):
        if current_player == gotypes.Player.white:
            self.ui.verticalWidget.setStyleSheet('#verticalWidget{border:1px solid blue;}')
            self.ui.verticalWidget_2.setStyleSheet("#verticalWidget_2{border:none}")
        else:
            self.ui.verticalWidget_2.setStyleSheet("#verticalWidget_2{border:1px solid blue;}")
            self.ui.verticalWidget.setStyleSheet('#verticalWidget{none}')

    def closeEvent(self, event):
        self.reset = 1
        super().closeEvent(event)

    def evaluate_territory_action(self, game_state):
        if game_state:  # Asigură-te că există o instanță de tablă de Go
            winner, scores = game_state.evaluate_territory()
            black_score = scores[Player.black]
            white_score = scores[Player.white]
            territory_message = f"Black Territory: {black_score}, White Territory: {white_score}"
            self.ui.textEdit_Probs.setText(territory_message)
            self.ui.label.setText(f"GAME OVER - {winner}")
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
    GoWindowController.adjust_scale_factor()

    # Generearea instanței reale pentru aplicație
    app = QtWidgets.QApplication(sys.argv)
    # Instantiere obiect
    ui = GoWindowController()
    # Afisare obiect in fereastra deschisa larg
    ui.show()
    # Inchidere aplicatie
    sys.exit(app.exec_())
