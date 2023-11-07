# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui\designs\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1009)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_GoBoard = QtWidgets.QWidget(self.centralwidget)
        self.widget_GoBoard.setGeometry(QtCore.QRect(20, 60, 900, 900))
        self.widget_GoBoard.setMinimumSize(QtCore.QSize(800, 800))
        self.widget_GoBoard.setMaximumSize(QtCore.QSize(900, 900))
        self.widget_GoBoard.setObjectName("widget_GoBoard")
        self.graphicsView_GoBoard = QtWidgets.QGraphicsView(self.widget_GoBoard)
        self.graphicsView_GoBoard.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
        self.graphicsView_GoBoard.setMinimumSize(QtCore.QSize(900, 900))
        self.graphicsView_GoBoard.setMaximumSize(QtCore.QSize(1000, 1000))
        self.graphicsView_GoBoard.setStyleSheet("background-color: rgb(200, 184, 135)")
        self.graphicsView_GoBoard.setObjectName("graphicsView_GoBoard")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 901, 28))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_Move = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_Move.setObjectName("label_Move")
        self.horizontalLayout.addWidget(self.label_Move, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_MoveNumber = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_MoveNumber.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_MoveNumber.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_MoveNumber.setAutoFillBackground(False)
        self.lineEdit_MoveNumber.setFrame(False)
        self.lineEdit_MoveNumber.setObjectName("lineEdit_MoveNumber")
        self.horizontalLayout.addWidget(self.lineEdit_MoveNumber, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_CurrentPlayer = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_CurrentPlayer.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_CurrentPlayer.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_CurrentPlayer.setFrame(False)
        self.lineEdit_CurrentPlayer.setObjectName("lineEdit_CurrentPlayer")
        self.horizontalLayout.addWidget(self.lineEdit_CurrentPlayer)
        self.lineEdit_MoveCoords = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_MoveCoords.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_MoveCoords.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_MoveCoords.setFrame(False)
        self.lineEdit_MoveCoords.setObjectName("lineEdit_MoveCoords")
        self.horizontalLayout.addWidget(self.lineEdit_MoveCoords)
        self.lineEdit_NextPlayer = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_NextPlayer.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_NextPlayer.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_NextPlayer.setFrame(False)
        self.lineEdit_NextPlayer.setObjectName("lineEdit_NextPlayer")
        self.horizontalLayout.addWidget(self.lineEdit_NextPlayer)
        self.label_NextPlyer = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_NextPlyer.setObjectName("label_NextPlyer")
        self.horizontalLayout.addWidget(self.label_NextPlyer)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.widget_IconToraGo = QtWidgets.QWidget(self.centralwidget)
        self.widget_IconToraGo.setGeometry(QtCore.QRect(930, 10, 970, 80))
        self.widget_IconToraGo.setMinimumSize(QtCore.QSize(970, 80))
        self.widget_IconToraGo.setMaximumSize(QtCore.QSize(970, 80))
        self.widget_IconToraGo.setStyleSheet("border: 1px solid black")
        self.widget_IconToraGo.setObjectName("widget_IconToraGo")
        self.widget_GameTree = QtWidgets.QWidget(self.centralwidget)
        self.widget_GameTree.setGeometry(QtCore.QRect(930, 769, 971, 191))
        self.widget_GameTree.setMinimumSize(QtCore.QSize(971, 191))
        self.widget_GameTree.setMaximumSize(QtCore.QSize(971, 191))
        self.widget_GameTree.setStyleSheet("border: 1px solid black")
        self.widget_GameTree.setObjectName("widget_GameTree")
        self.widget_Menu = QtWidgets.QWidget(self.centralwidget)
        self.widget_Menu.setGeometry(QtCore.QRect(930, 120, 971, 400))
        self.widget_Menu.setMinimumSize(QtCore.QSize(971, 400))
        self.widget_Menu.setMaximumSize(QtCore.QSize(971, 400))
        self.widget_Menu.setStyleSheet("border: 1px solid black;")
        self.widget_Menu.setObjectName("widget_Menu")
        self.widget_MoveOptions = QtWidgets.QWidget(self.centralwidget)
        self.widget_MoveOptions.setGeometry(QtCore.QRect(930, 700, 970, 61))
        self.widget_MoveOptions.setMinimumSize(QtCore.QSize(970, 61))
        self.widget_MoveOptions.setMaximumSize(QtCore.QSize(970, 61))
        self.widget_MoveOptions.setObjectName("widget_MoveOptions")
        self.layoutWidget = QtWidgets.QWidget(self.widget_MoveOptions)
        self.layoutWidget.setGeometry(QtCore.QRect(350, 0, 271, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layoutWidget.sizePolicy().hasHeightForWidth())
        self.layoutWidget.setSizePolicy(sizePolicy)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMinimumSize(QtCore.QSize(60, 50))
        self.pushButton_6.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_6.setAutoDefault(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMinimumSize(QtCore.QSize(30, 50))
        self.pushButton_4.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QtCore.QSize(60, 50))
        self.pushButton_3.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMinimumSize(QtCore.QSize(60, 50))
        self.pushButton_5.setMaximumSize(QtCore.QSize(60, 50))
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_5.setAutoDefault(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.widget_Players = QtWidgets.QWidget(self.centralwidget)
        self.widget_Players.setGeometry(QtCore.QRect(930, 600, 971, 93))
        self.widget_Players.setObjectName("widget_Players")
        self.layoutWidget1 = QtWidgets.QWidget(self.widget_Players)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 971, 93))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_Players = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_Players.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_Players.setObjectName("horizontalLayout_Players")
        self.widget_PlayerWhite = QtWidgets.QWidget(self.layoutWidget1)
        self.widget_PlayerWhite.setMinimumSize(QtCore.QSize(461, 91))
        self.widget_PlayerWhite.setMaximumSize(QtCore.QSize(461, 91))
        self.widget_PlayerWhite.setStyleSheet("border:  1px solid grey;")
        self.widget_PlayerWhite.setObjectName("widget_PlayerWhite")
        self.labelW = QtWidgets.QLabel(self.widget_PlayerWhite)
        self.labelW.setGeometry(QtCore.QRect(90, 0, 371, 45))
        self.labelW.setMinimumSize(QtCore.QSize(371, 45))
        self.labelW.setMaximumSize(QtCore.QSize(371, 48))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.labelW.setFont(font)
        self.labelW.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelW.setStyleSheet("background:white;\n"
"border-bottom:1px solid black;")
        self.labelW.setTextFormat(QtCore.Qt.AutoText)
        self.labelW.setScaledContents(True)
        self.labelW.setAlignment(QtCore.Qt.AlignCenter)
        self.labelW.setObjectName("labelW")
        self.label_IconW = QtWidgets.QLabel(self.widget_PlayerWhite)
        self.label_IconW.setGeometry(QtCore.QRect(0, 0, 91, 91))
        self.label_IconW.setMinimumSize(QtCore.QSize(91, 91))
        self.label_IconW.setMaximumSize(QtCore.QSize(91, 91))
        self.label_IconW.setText("")
        self.label_IconW.setPixmap(QtGui.QPixmap(".\\gui\\designs\\../resources/TigerW.jpg"))
        self.label_IconW.setScaledContents(True)
        self.label_IconW.setObjectName("label_IconW")
        self.label_CapturesW = QtWidgets.QLabel(self.widget_PlayerWhite)
        self.label_CapturesW.setGeometry(QtCore.QRect(-1, 45, 461, 45))
        self.label_CapturesW.setMinimumSize(QtCore.QSize(461, 45))
        self.label_CapturesW.setMaximumSize(QtCore.QSize(461, 45))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_CapturesW.setFont(font)
        self.label_CapturesW.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_CapturesW.setStyleSheet("background: grey;\n"
"border-top: 1px solid white;")
        self.label_CapturesW.setText("")
        self.label_CapturesW.setTextFormat(QtCore.Qt.AutoText)
        self.label_CapturesW.setScaledContents(True)
        self.label_CapturesW.setAlignment(QtCore.Qt.AlignCenter)
        self.label_CapturesW.setObjectName("label_CapturesW")
        self.labelW.raise_()
        self.label_CapturesW.raise_()
        self.label_IconW.raise_()
        self.horizontalLayout_Players.addWidget(self.widget_PlayerWhite)
        self.widget_PlayerBlack = QtWidgets.QWidget(self.layoutWidget1)
        self.widget_PlayerBlack.setMinimumSize(QtCore.QSize(471, 91))
        self.widget_PlayerBlack.setMaximumSize(QtCore.QSize(471, 91))
        self.widget_PlayerBlack.setStyleSheet("border:1px solid grey;")
        self.widget_PlayerBlack.setObjectName("widget_PlayerBlack")
        self.label_B = QtWidgets.QLabel(self.widget_PlayerBlack)
        self.label_B.setGeometry(QtCore.QRect(0, 0, 381, 51))
        self.label_B.setMinimumSize(QtCore.QSize(381, 51))
        self.label_B.setMaximumSize(QtCore.QSize(381, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_B.setFont(font)
        self.label_B.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_B.setStyleSheet("color:white;\n"
"background:black;")
        self.label_B.setTextFormat(QtCore.Qt.AutoText)
        self.label_B.setScaledContents(True)
        self.label_B.setAlignment(QtCore.Qt.AlignCenter)
        self.label_B.setObjectName("label_B")
        self.label_IconB = QtWidgets.QLabel(self.widget_PlayerBlack)
        self.label_IconB.setGeometry(QtCore.QRect(380, 0, 91, 91))
        self.label_IconB.setMinimumSize(QtCore.QSize(91, 91))
        self.label_IconB.setMaximumSize(QtCore.QSize(91, 91))
        self.label_IconB.setText("")
        self.label_IconB.setPixmap(QtGui.QPixmap(".\\gui\\designs\\../resources/TigerB.jpg"))
        self.label_IconB.setScaledContents(True)
        self.label_IconB.setObjectName("label_IconB")
        self.label_CapturesB = QtWidgets.QLabel(self.widget_PlayerBlack)
        self.label_CapturesB.setGeometry(QtCore.QRect(-1, 45, 471, 51))
        self.label_CapturesB.setMinimumSize(QtCore.QSize(471, 51))
        self.label_CapturesB.setMaximumSize(QtCore.QSize(471, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_CapturesB.setFont(font)
        self.label_CapturesB.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_CapturesB.setStyleSheet("background: grey;\n"
"border-top: 1px solid white;")
        self.label_CapturesB.setText("")
        self.label_CapturesB.setTextFormat(QtCore.Qt.AutoText)
        self.label_CapturesB.setScaledContents(True)
        self.label_CapturesB.setAlignment(QtCore.Qt.AlignCenter)
        self.label_CapturesB.setObjectName("label_CapturesB")
        self.label_B.raise_()
        self.label_CapturesB.raise_()
        self.label_IconB.raise_()
        self.horizontalLayout_Players.addWidget(self.widget_PlayerBlack)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_Move.setText(_translate("MainWindow", "Move "))
        self.label_NextPlyer.setText(_translate("MainWindow", "to play"))
        self.pushButton_6.setText(_translate("MainWindow", "<<"))
        self.pushButton_4.setText(_translate("MainWindow", "<"))
        self.pushButton_3.setText(_translate("MainWindow", ">"))
        self.pushButton_5.setText(_translate("MainWindow", ">>"))
        self.labelW.setText(_translate("MainWindow", "White"))
        self.label_B.setText(_translate("MainWindow", "Black"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
