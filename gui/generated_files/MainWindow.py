# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui\designs\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1666, 1153)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.toolButton = QtWidgets.QToolButton(self.widget)
        self.toolButton.setMinimumSize(QtCore.QSize(30, 30))
        self.toolButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolButton.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButton.setObjectName("toolButton")
        self.verticalLayout_2.addWidget(self.toolButton)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.widget_GoBoard = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_GoBoard.sizePolicy().hasHeightForWidth())
        self.widget_GoBoard.setSizePolicy(sizePolicy)
        self.widget_GoBoard.setMinimumSize(QtCore.QSize(900, 900))
        self.widget_GoBoard.setMaximumSize(QtCore.QSize(900, 900))
        self.widget_GoBoard.setStyleSheet("background-color: rgb(200, 184, 135)")
        self.widget_GoBoard.setObjectName("widget_GoBoard")
        self.graphicsView_GoBoard = QtWidgets.QGraphicsView(self.widget_GoBoard)
        self.graphicsView_GoBoard.setGeometry(QtCore.QRect(0, 0, 900, 900))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_GoBoard.sizePolicy().hasHeightForWidth())
        self.graphicsView_GoBoard.setSizePolicy(sizePolicy)
        self.graphicsView_GoBoard.setMinimumSize(QtCore.QSize(900, 900))
        self.graphicsView_GoBoard.setMaximumSize(QtCore.QSize(900, 900))
        self.graphicsView_GoBoard.setStyleSheet("background-color: rgb(200, 184, 135)")
        self.graphicsView_GoBoard.setObjectName("graphicsView_GoBoard")
        self.widget_gameStarter = QtWidgets.QWidget(self.widget_GoBoard)
        self.widget_gameStarter.setGeometry(QtCore.QRect(220, 370, 421, 55))
        self.widget_gameStarter.setMinimumSize(QtCore.QSize(0, 20))
        self.widget_gameStarter.setMaximumSize(QtCore.QSize(450, 55))
        self.widget_gameStarter.setAutoFillBackground(True)
        self.widget_gameStarter.setStyleSheet("background:light;")
        self.widget_gameStarter.setObjectName("widget_gameStarter")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_gameStarter)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_middleBoard = QtWidgets.QLabel(self.widget_gameStarter)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_middleBoard.setFont(font)
        self.label_middleBoard.setObjectName("label_middleBoard")
        self.gridLayout.addWidget(self.label_middleBoard, 0, 0, 1, 1)
        self.spinBox_numberOfSimulations = QtWidgets.QSpinBox(self.widget_gameStarter)
        self.spinBox_numberOfSimulations.setMinimumSize(QtCore.QSize(70, 30))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 1))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 1))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.spinBox_numberOfSimulations.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.spinBox_numberOfSimulations.setFont(font)
        self.spinBox_numberOfSimulations.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.spinBox_numberOfSimulations.setWhatsThis("")
        self.spinBox_numberOfSimulations.setAutoFillBackground(True)
        self.spinBox_numberOfSimulations.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.spinBox_numberOfSimulations.setWrapping(False)
        self.spinBox_numberOfSimulations.setFrame(False)
        self.spinBox_numberOfSimulations.setAccelerated(True)
        self.spinBox_numberOfSimulations.setKeyboardTracking(False)
        self.spinBox_numberOfSimulations.setMinimum(1)
        self.spinBox_numberOfSimulations.setMaximum(500)
        self.spinBox_numberOfSimulations.setObjectName("spinBox_numberOfSimulations")
        self.gridLayout.addWidget(self.spinBox_numberOfSimulations, 0, 1, 1, 1)
        self.pushButton_StartGame = QtWidgets.QPushButton(self.widget_gameStarter)
        self.pushButton_StartGame.setMinimumSize(QtCore.QSize(70, 40))
        self.pushButton_StartGame.setMaximumSize(QtCore.QSize(70, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_StartGame.setFont(font)
        self.pushButton_StartGame.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_StartGame.setObjectName("pushButton_StartGame")
        self.gridLayout.addWidget(self.pushButton_StartGame, 0, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.widget_GoBoard, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout.addWidget(self.widget, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(2, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy)
        self.widget1.setMinimumSize(QtCore.QSize(600, 1073))
        self.widget1.setMaximumSize(QtCore.QSize(1000, 1080))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_game = QtWidgets.QLabel(self.widget1)
        self.label_game.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_game.setFont(font)
        self.label_game.setStyleSheet("color:brown")
        self.label_game.setText("")
        self.label_game.setScaledContents(True)
        self.label_game.setWordWrap(True)
        self.label_game.setObjectName("label_game")
        self.verticalLayout_5.addWidget(self.label_game, 0, QtCore.Qt.AlignTop)
        self.widget_9 = QtWidgets.QWidget(self.widget1)
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_9)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_best5Moves = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_best5Moves.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_best5Moves.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_best5Moves.setAutoFillBackground(True)
        self.pushButton_best5Moves.setFlat(False)
        self.pushButton_best5Moves.setObjectName("pushButton_best5Moves")
        self.horizontalLayout_6.addWidget(self.pushButton_best5Moves)
        self.pushButton_PlayStop = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_PlayStop.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_PlayStop.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_PlayStop.setObjectName("pushButton_PlayStop")
        self.horizontalLayout_6.addWidget(self.pushButton_PlayStop)
        self.pushButton_EndSimulations = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_EndSimulations.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_EndSimulations.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_EndSimulations.setAutoFillBackground(True)
        self.pushButton_EndSimulations.setFlat(False)
        self.pushButton_EndSimulations.setObjectName("pushButton_EndSimulations")
        self.horizontalLayout_6.addWidget(self.pushButton_EndSimulations)
        self.pushButton_SaveGame = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_SaveGame.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_SaveGame.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_SaveGame.setAutoFillBackground(True)
        self.pushButton_SaveGame.setFlat(False)
        self.pushButton_SaveGame.setObjectName("pushButton_SaveGame")
        self.horizontalLayout_6.addWidget(self.pushButton_SaveGame)
        self.verticalLayout_5.addWidget(self.widget_9)
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2, 0, QtCore.Qt.AlignTop)
        self.horizontalSlider = QtWidgets.QSlider(self.widget1)
        self.horizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalSlider.setMinimum(100)
        self.horizontalSlider.setMaximum(3100)
        self.horizontalSlider.setSingleStep(500)
        self.horizontalSlider.setPageStep(500)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(True)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(500)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_5.addWidget(self.horizontalSlider)
        self.line = QtWidgets.QFrame(self.widget1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_5.addWidget(self.line)
        self.horizontalWidget_2 = QtWidgets.QWidget(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget_2.sizePolicy().hasHeightForWidth())
        self.horizontalWidget_2.setSizePolicy(sizePolicy)
        self.horizontalWidget_2.setMinimumSize(QtCore.QSize(0, 300))
        self.horizontalWidget_2.setMaximumSize(QtCore.QSize(16777215, 300))
        self.horizontalWidget_2.setObjectName("horizontalWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_2 = QtWidgets.QWidget(self.horizontalWidget_2)
        self.widget_2.setMinimumSize(QtCore.QSize(242, 209))
        self.widget_2.setObjectName("widget_2")
        self.verticalWidget = QtWidgets.QWidget(self.widget_2)
        self.verticalWidget.setGeometry(QtCore.QRect(9, 0, 231, 261))
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_2.setStyleSheet("\n"
"background-color: rgba(255, 255, 255, 0);")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_3.addWidget(self.lineEdit_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_IconB = QtWidgets.QLabel(self.verticalWidget)
        self.label_IconB.setEnabled(True)
        self.label_IconB.setMinimumSize(QtCore.QSize(100, 100))
        self.label_IconB.setMaximumSize(QtCore.QSize(100, 100))
        self.label_IconB.setText("")
        self.label_IconB.setScaledContents(True)
        self.label_IconB.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_IconB.setWordWrap(False)
        self.label_IconB.setObjectName("label_IconB")
        self.verticalLayout_3.addWidget(self.label_IconB, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.BlackPlayerName = QtWidgets.QLineEdit(self.verticalWidget)
        self.BlackPlayerName.setMinimumSize(QtCore.QSize(114, 19))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.BlackPlayerName.setFont(font)
        self.BlackPlayerName.setFrame(False)
        self.BlackPlayerName.setAlignment(QtCore.Qt.AlignCenter)
        self.BlackPlayerName.setReadOnly(True)
        self.BlackPlayerName.setObjectName("BlackPlayerName")
        self.verticalLayout_3.addWidget(self.BlackPlayerName, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.lineEdit_BlackCaptures = QtWidgets.QLineEdit(self.verticalWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.lineEdit_BlackCaptures.setFont(font)
        self.lineEdit_BlackCaptures.setStyleSheet("background:transparent;")
        self.lineEdit_BlackCaptures.setFrame(False)
        self.lineEdit_BlackCaptures.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_BlackCaptures.setReadOnly(True)
        self.lineEdit_BlackCaptures.setObjectName("lineEdit_BlackCaptures")
        self.verticalLayout_3.addWidget(self.lineEdit_BlackCaptures, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.horizontalLayout_3.addWidget(self.widget_2, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.widget_3 = QtWidgets.QWidget(self.horizontalWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QtCore.QSize(241, 150))
        self.widget_3.setObjectName("widget_3")
        self.verticalWidget_2 = QtWidgets.QWidget(self.widget_3)
        self.verticalWidget_2.setGeometry(QtCore.QRect(0, 0, 241, 261))
        self.verticalWidget_2.setObjectName("verticalWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalWidget_2)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.verticalWidget_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_4.setStyleSheet("\n"
"background-color: rgba(255, 255, 255, 0);")
        self.lineEdit_4.setFrame(False)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_4.addWidget(self.lineEdit_4, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_IconW = QtWidgets.QLabel(self.verticalWidget_2)
        self.label_IconW.setEnabled(True)
        self.label_IconW.setMinimumSize(QtCore.QSize(100, 100))
        self.label_IconW.setMaximumSize(QtCore.QSize(100, 100))
        self.label_IconW.setText("")
        self.label_IconW.setScaledContents(True)
        self.label_IconW.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_IconW.setWordWrap(False)
        self.label_IconW.setObjectName("label_IconW")
        self.verticalLayout_4.addWidget(self.label_IconW, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.WhitePlayerName = QtWidgets.QLineEdit(self.verticalWidget_2)
        self.WhitePlayerName.setMinimumSize(QtCore.QSize(114, 19))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.WhitePlayerName.setFont(font)
        self.WhitePlayerName.setText("")
        self.WhitePlayerName.setFrame(False)
        self.WhitePlayerName.setAlignment(QtCore.Qt.AlignCenter)
        self.WhitePlayerName.setReadOnly(True)
        self.WhitePlayerName.setObjectName("WhitePlayerName")
        self.verticalLayout_4.addWidget(self.WhitePlayerName, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.lineEdit_WhiteCaptures = QtWidgets.QLineEdit(self.verticalWidget_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.lineEdit_WhiteCaptures.setFont(font)
        self.lineEdit_WhiteCaptures.setStyleSheet("background:transparent;")
        self.lineEdit_WhiteCaptures.setFrame(False)
        self.lineEdit_WhiteCaptures.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_WhiteCaptures.setReadOnly(True)
        self.lineEdit_WhiteCaptures.setObjectName("lineEdit_WhiteCaptures")
        self.verticalLayout_4.addWidget(self.lineEdit_WhiteCaptures, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.horizontalLayout_3.addWidget(self.widget_3, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_5.addWidget(self.horizontalWidget_2)
        self.widget_5 = QtWidgets.QWidget(self.widget1)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pushButton = QtWidgets.QPushButton(self.widget_5)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_7.addWidget(self.pushButton)
        self.pushButton_Resign = QtWidgets.QPushButton(self.widget_5)
        self.pushButton_Resign.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_Resign.setObjectName("pushButton_Resign")
        self.horizontalLayout_7.addWidget(self.pushButton_Resign)
        self.verticalLayout_5.addWidget(self.widget_5)
        self.stackedWidget_Probs_TreeView = QtWidgets.QStackedWidget(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget_Probs_TreeView.sizePolicy().hasHeightForWidth())
        self.stackedWidget_Probs_TreeView.setSizePolicy(sizePolicy)
        self.stackedWidget_Probs_TreeView.setObjectName("stackedWidget_Probs_TreeView")
        self.page_Probs = QtWidgets.QWidget()
        self.page_Probs.setObjectName("page_Probs")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.page_Probs)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.textEdit_Probs = QtWidgets.QTextEdit(self.page_Probs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_Probs.sizePolicy().hasHeightForWidth())
        self.textEdit_Probs.setSizePolicy(sizePolicy)
        self.textEdit_Probs.setMinimumSize(QtCore.QSize(500, 450))
        self.textEdit_Probs.setMaximumSize(QtCore.QSize(16777215, 400))
        self.textEdit_Probs.setStyleSheet("background-color: rgb(214, 214, 160);")
        self.textEdit_Probs.setReadOnly(True)
        self.textEdit_Probs.setObjectName("textEdit_Probs")
        self.horizontalLayout_4.addWidget(self.textEdit_Probs, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.stackedWidget_Probs_TreeView.addWidget(self.page_Probs)
        self.page_TreeView = QtWidgets.QWidget()
        self.page_TreeView.setObjectName("page_TreeView")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_TreeView)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_4 = QtWidgets.QWidget(self.page_TreeView)
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 70))
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_firstMove = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_firstMove.setMinimumSize(QtCore.QSize(70, 50))
        self.pushButton_firstMove.setMaximumSize(QtCore.QSize(70, 50))
        self.pushButton_firstMove.setObjectName("pushButton_firstMove")
        self.horizontalLayout_2.addWidget(self.pushButton_firstMove)
        self.pushButton_prevMove = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_prevMove.setMinimumSize(QtCore.QSize(70, 50))
        self.pushButton_prevMove.setMaximumSize(QtCore.QSize(70, 50))
        self.pushButton_prevMove.setObjectName("pushButton_prevMove")
        self.horizontalLayout_2.addWidget(self.pushButton_prevMove)
        self.pushButton_nextMove = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_nextMove.setMinimumSize(QtCore.QSize(70, 50))
        self.pushButton_nextMove.setMaximumSize(QtCore.QSize(70, 50))
        self.pushButton_nextMove.setObjectName("pushButton_nextMove")
        self.horizontalLayout_2.addWidget(self.pushButton_nextMove)
        self.pushButton_lastMove = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_lastMove.setMinimumSize(QtCore.QSize(70, 50))
        self.pushButton_lastMove.setMaximumSize(QtCore.QSize(70, 50))
        self.pushButton_lastMove.setObjectName("pushButton_lastMove")
        self.horizontalLayout_2.addWidget(self.pushButton_lastMove)
        self.verticalLayout_6.addWidget(self.widget_4, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.graphicsView_GameTree = QtWidgets.QGraphicsView(self.page_TreeView)
        self.graphicsView_GameTree.setObjectName("graphicsView_GameTree")
        self.verticalLayout_6.addWidget(self.graphicsView_GameTree)
        self.stackedWidget_Probs_TreeView.addWidget(self.page_TreeView)
        self.verticalLayout_5.addWidget(self.stackedWidget_Probs_TreeView)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.label_FinalResults = QtWidgets.QLabel(self.widget1)
        self.label_FinalResults.setObjectName("label_FinalResults")
        self.verticalLayout_5.addWidget(self.label_FinalResults)
        self.horizontalLayout.addWidget(self.widget1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1666, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar.addSeparator()
        self.label_middleBoard.setBuddy(self.spinBox_numberOfSimulations)

        self.retranslateUi(MainWindow)
        self.stackedWidget_Probs_TreeView.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "Moves info"))
        self.label_middleBoard.setText(_translate("MainWindow", "Number of episodes to simulate"))
        self.pushButton_StartGame.setText(_translate("MainWindow", "Start"))
        self.pushButton_best5Moves.setText(_translate("MainWindow", "See Best 5"))
        self.pushButton_PlayStop.setText(_translate("MainWindow", "Stop Game"))
        self.pushButton_EndSimulations.setText(_translate("MainWindow", "End Simulations "))
        self.pushButton_SaveGame.setText(_translate("MainWindow", "Save Game"))
        self.label_2.setText(_translate("MainWindow", "Playing Speed"))
        self.lineEdit_2.setText(_translate("MainWindow", "BLACK"))
        self.BlackPlayerName.setStyleSheet(_translate("MainWindow", "\n"
"background-color: rgba(255, 255, 255, 0);"))
        self.BlackPlayerName.setPlaceholderText(_translate("MainWindow", "Black Player"))
        self.lineEdit_4.setText(_translate("MainWindow", "WHITE"))
        self.WhitePlayerName.setStyleSheet(_translate("MainWindow", "\n"
"background-color: rgba(255, 255, 255, 0);"))
        self.WhitePlayerName.setPlaceholderText(_translate("MainWindow", "White Player"))
        self.pushButton.setText(_translate("MainWindow", "PASS"))
        self.pushButton_Resign.setText(_translate("MainWindow", "RESIGN"))
        self.textEdit_Probs.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_firstMove.setText(_translate("MainWindow", "<<"))
        self.pushButton_prevMove.setText(_translate("MainWindow", "<"))
        self.pushButton_nextMove.setText(_translate("MainWindow", ">"))
        self.pushButton_lastMove.setText(_translate("MainWindow", ">>"))
        self.label_FinalResults.setText(_translate("MainWindow", "LabelFinalResult"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
