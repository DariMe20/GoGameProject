import os
import sys
from PyQt5 import QtWidgets

from gui.controllers.GoWindowController import GoWindowController
from gui.generated_files.MainMenuPage import Ui_MainWindow
from utils import constants


class MainMenuPageController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_CreateSGF.clicked.connect(self.createSGF)
        self.ui.pushButton_EditSGF.clicked.connect(self.editSGF)
        self.ui.pushButton_PlayerVSBot.clicked.connect(self.playerVSbot)
        self.ui.pushButton_BotVBot.clicked.connect(self.bot_vs_bot_settings)

        self.ui.comboBox_BlackBot.addItems(list(constants.BOTS.keys()))
        self.ui.comboBox_WhiteBot.addItems(list(constants.BOTS.keys()))

        self.GoGameWindow = None

    def createSGF(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.pushButton_CreateOk.clicked.connect(self.createSGF_game)

    def createSGF_game(self):
        nameW = self.ui.lineEdit_WhiteName.text()
        nameB = self.ui.lineEdit_BlackName.text()
        board_size = self.ui.spinBox_BoardSize.value()
        handicap = self.ui.spinBox_Handicap.value()
        komi = self.ui.doubleSpinBox_Komi.value()

        try:
            self.GoGameWindow = GoWindowController(nameB, nameW, 1, 0, board_size, handicap, komi)
            self.GoGameWindow.show()
        except Exception as e:
            print(f"Error in bot vs bot create: {e}")


    def editSGF(self):
        pass

    def playerVSbot(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.pushButton_PlayWithBotOk.clicked.connect(self.playerVSbot_game)

    def playerVSbot_game(self):
        if self.ui.radioButton_Black.isChecked():
            nameB = "You"
            nameW = "Bot"
            player_color = 0
        elif self.ui.radioButton_White.isChecked():
            nameB = "Bot"
            nameW = "You"
            player_color = 1
        else:
            QtWidgets.QMessageBox.critical(self, "Eroare de selecție", "Te rog alege culoarea cu care dorești să joci!")
            return

        board_size = self.ui.spinBox_BoardSizeP.value()
        handicap = self.ui.spinBox_HandicapP.value()
        komi = self.ui.doubleSpinBox_KomiP.value()

        try:
            self.GoGameWindow = GoWindowController(nameB, nameW, 3, player_color, board_size, handicap, komi)
            self.GoGameWindow.show()
        except Exception as e:
            print(f"Error in bot vs bot create: {e}")

    def bot_vs_bot_settings(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.pushButton_BotVsBotOK.clicked.connect(self.botVSbot)

    def botVSbot(self):
        try:
            black_name = self.ui.comboBox_BlackBot.currentText()
            white_name = self.ui.comboBox_WhiteBot.currentText()

            self.GoGameWindow = GoWindowController(black_name, white_name, 4)
            # Afisează fereastra
            self.GoGameWindow.show()
        except Exception as e:
            print(f"Error in bot vs bot create: {e}")


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
    MainMenuPageController.adjust_scale_factor()
    # Generearea instanței reale pentru aplicație
    app = QtWidgets.QApplication(sys.argv)
    # Instantiere obiect
    ui = MainMenuPageController()
    # Afisare obiect in fereastra deschisa larg
    ui.show()
    # Inchidere aplicatie
    sys.exit(app.exec_())