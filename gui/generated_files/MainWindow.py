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
        MainWindow.resize(1428, 1192)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_MenuButtons = QtWidgets.QWidget(self.centralwidget)
        self.widget_MenuButtons.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_MenuButtons.setObjectName("widget_MenuButtons")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_MenuButtons)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_CreateSGF = QtWidgets.QPushButton(self.widget_MenuButtons)
        self.pushButton_CreateSGF.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_CreateSGF.setFont(font)
        self.pushButton_CreateSGF.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_CreateSGF.setStyleSheet("border: 1px solid black;\n"
"border-radius: 10px;\n"
"background: rgba(255, 241, 224, 180)")
        self.pushButton_CreateSGF.setObjectName("pushButton_CreateSGF")
        self.horizontalLayout_2.addWidget(self.pushButton_CreateSGF, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_MenuButtons)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("border: 1px solid black;\n"
"border-radius: 10px;\n"
"background: rgba(255, 241, 224, 180)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_PlayBot = QtWidgets.QPushButton(self.widget_MenuButtons)
        self.pushButton_PlayBot.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_PlayBot.setFont(font)
        self.pushButton_PlayBot.setStyleSheet("border: 1px solid black;\n"
"border-radius: 10px;\n"
"background: rgba(255, 241, 224, 180)")
        self.pushButton_PlayBot.setObjectName("pushButton_PlayBot")
        self.horizontalLayout_2.addWidget(self.pushButton_PlayBot)
        self.pushButton_BotVBot = QtWidgets.QPushButton(self.widget_MenuButtons)
        self.pushButton_BotVBot.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_BotVBot.setFont(font)
        self.pushButton_BotVBot.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_BotVBot.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_BotVBot.setStyleSheet("border: 1px solid black;\n"
"border-radius: 10px;\n"
"background: rgba(255, 241, 224, 180)")
        self.pushButton_BotVBot.setCheckable(False)
        self.pushButton_BotVBot.setAutoDefault(True)
        self.pushButton_BotVBot.setDefault(True)
        self.pushButton_BotVBot.setObjectName("pushButton_BotVBot")
        self.horizontalLayout_2.addWidget(self.pushButton_BotVBot, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_9 = QtWidgets.QPushButton(self.widget_MenuButtons)
        self.pushButton_9.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setStyleSheet("border: 1px solid black;\n"
"border-radius: 10px;\n"
"background: rgba(255, 241, 224, 180)")
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_2.addWidget(self.pushButton_9, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.widget_MenuButtons)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_GoBoard = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_GoBoard.sizePolicy().hasHeightForWidth())
        self.widget_GoBoard.setSizePolicy(sizePolicy)
        self.widget_GoBoard.setMinimumSize(QtCore.QSize(900, 900))
        self.widget_GoBoard.setMaximumSize(QtCore.QSize(850, 850))
        self.widget_GoBoard.setStyleSheet("background-color: rgb(200, 184, 135)")
        self.widget_GoBoard.setObjectName("widget_GoBoard")
        self.graphicsView_GoBoard = QtWidgets.QGraphicsView(self.widget_GoBoard)
        self.graphicsView_GoBoard.setGeometry(QtCore.QRect(0, 0, 900, 900))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_GoBoard.sizePolicy().hasHeightForWidth())
        self.graphicsView_GoBoard.setSizePolicy(sizePolicy)
        self.graphicsView_GoBoard.setMinimumSize(QtCore.QSize(900, 900))
        self.graphicsView_GoBoard.setMaximumSize(QtCore.QSize(900, 900))
        self.graphicsView_GoBoard.setStyleSheet("background-color: rgb(200, 184, 135)")
        self.graphicsView_GoBoard.setObjectName("graphicsView_GoBoard")
        self.verticalLayout_2.addWidget(self.widget_GoBoard, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(500, 1073))
        self.widget.setObjectName("widget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 110, 501, 261))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_2 = QtWidgets.QWidget(self.horizontalLayoutWidget_2)
        self.widget_2.setMinimumSize(QtCore.QSize(242, 209))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.widget_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, 0, 241, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
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
        self.label_IconB = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_IconB.setEnabled(True)
        self.label_IconB.setMinimumSize(QtCore.QSize(100, 100))
        self.label_IconB.setMaximumSize(QtCore.QSize(100, 100))
        self.label_IconB.setText("")
        self.label_IconB.setScaledContents(True)
        self.label_IconB.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_IconB.setWordWrap(False)
        self.label_IconB.setObjectName("label_IconB")
        self.verticalLayout_3.addWidget(self.label_IconB, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.PlayerName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.PlayerName.setMinimumSize(QtCore.QSize(114, 19))
        self.PlayerName.setFrame(False)
        self.PlayerName.setAlignment(QtCore.Qt.AlignCenter)
        self.PlayerName.setReadOnly(True)
        self.PlayerName.setObjectName("PlayerName")
        self.verticalLayout_3.addWidget(self.PlayerName, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_3.addWidget(self.lineEdit_3, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.horizontalLayout_3.addWidget(self.widget_2, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.widget_3 = QtWidgets.QWidget(self.horizontalLayoutWidget_2)
        self.widget_3.setMinimumSize(QtCore.QSize(241, 209))
        self.widget_3.setObjectName("widget_3")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.widget_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 241, 261))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
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
        self.label_IconW = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_IconW.setEnabled(True)
        self.label_IconW.setMinimumSize(QtCore.QSize(100, 100))
        self.label_IconW.setMaximumSize(QtCore.QSize(100, 100))
        self.label_IconW.setText("")
        self.label_IconW.setScaledContents(True)
        self.label_IconW.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_IconW.setWordWrap(False)
        self.label_IconW.setObjectName("label_IconW")
        self.verticalLayout_4.addWidget(self.label_IconW, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.PlayerName_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.PlayerName_2.setMinimumSize(QtCore.QSize(114, 19))
        self.PlayerName_2.setText("")
        self.PlayerName_2.setFrame(False)
        self.PlayerName_2.setAlignment(QtCore.Qt.AlignCenter)
        self.PlayerName_2.setReadOnly(True)
        self.PlayerName_2.setObjectName("PlayerName_2")
        self.verticalLayout_4.addWidget(self.PlayerName_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout_4.addWidget(self.lineEdit_5, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.horizontalLayout_3.addWidget(self.widget_3, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout.addWidget(self.widget, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1428, 22))
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
        self.pushButton_CreateSGF.setText(_translate("MainWindow", "Create SGF"))
        self.pushButton_2.setText(_translate("MainWindow", "Edit SGF"))
        self.pushButton_PlayBot.setText(_translate("MainWindow", "Play with Bot"))
        self.pushButton_BotVBot.setText(_translate("MainWindow", "Bot VS Bot"))
        self.pushButton_9.setText(_translate("MainWindow", "About GO"))
        self.lineEdit_2.setText(_translate("MainWindow", "BLACK"))
        self.PlayerName.setStyleSheet(_translate("MainWindow", "\n"
"background-color: rgba(255, 255, 255, 0);"))
        self.PlayerName.setPlaceholderText(_translate("MainWindow", "Black Player"))
        self.lineEdit_4.setText(_translate("MainWindow", "WHITE"))
        self.PlayerName_2.setStyleSheet(_translate("MainWindow", "\n"
"background-color: rgba(255, 255, 255, 0);"))
        self.PlayerName_2.setPlaceholderText(_translate("MainWindow", "White Player"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
