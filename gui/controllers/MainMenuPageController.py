import os
import sys
from PyQt5 import QtWidgets

from gui.controllers.MainWindowController import MainWindowController
from gui.generated_files.MainMenuPage import Ui_MainWindow


class MainMenuPageController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_CreateSGF.clicked.connect(self.createSGF)
        self.ui.pushButton_EditSGF.clicked.connect(self.editSGF)
        self.ui.pushButton_PlayerVSBot.clicked.connect(self.playerVSbot)
        self.ui.pushButton_BotVBot.clicked.connect(self.botVSbot)

        self.GoGameWindow = None

    def createSGF(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def editSGF(self):
        pass

    def playerVSbot(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def botVSbot(self):
        try:
            if self.GoGameWindow is None:
                self.GoGameWindow = MainWindowController()
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