from PyQt5 import QtWidgets

from gui.generated_files.MainWindow import Ui_MainWindow


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ui = MainWindowController()
    ui.showMaximized()
    app.exec_()
