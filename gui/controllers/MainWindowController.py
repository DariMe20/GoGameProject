from PyQt5 import QtWidgets, QtCore
from gui.generated_files.MainWindow import Ui_MainWindow
from gui.section_controllers.GoBoardController import GoBoardController


class MainWindowController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.board = None
        self.scene = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.board_size = 13
        self.init_GoBoard()

    def init_GoBoard(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.board = GoBoardController(self.board_size)
        self.scene.addItem(self.board)
        self.scene.setSceneRect(0, 0, 880, 880)  # Updated to match GoBoardController's boundingRect dimensions
        self.ui.graphicsView_GoBoard.setScene(self.scene)
        self.ui.graphicsView_GoBoard.setViewportMargins(0, 0, 0, 0)
        self.ui.graphicsView_GoBoard.centerOn(450, 450)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ui = MainWindowController()
    ui.showMaximized()
    app.exec_()
