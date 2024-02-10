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
        MainWindow.resize(1454, 1168)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.pushButton_StartGame = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_StartGame.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_StartGame.setObjectName("pushButton_StartGame")
        self.verticalLayout_2.addWidget(self.pushButton_StartGame, 0, QtCore.Qt.AlignHCenter)
        self.widget_GoBoard = QtWidgets.QWidget(self.centralwidget)
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
        self.verticalLayout_2.addWidget(self.widget_GoBoard, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(500, 1073))
        self.widget.setObjectName("widget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 110, 501, 261))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_2 = QtWidgets.QWidget(self.horizontalLayoutWidget_2)
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
        self.BlackPlayerName.setFrame(False)
        self.BlackPlayerName.setAlignment(QtCore.Qt.AlignCenter)
        self.BlackPlayerName.setReadOnly(True)
        self.BlackPlayerName.setObjectName("BlackPlayerName")
        self.verticalLayout_3.addWidget(self.BlackPlayerName, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.lineEdit_BlackCaptures = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_BlackCaptures.setReadOnly(True)
        self.lineEdit_BlackCaptures.setObjectName("lineEdit_BlackCaptures")
        self.verticalLayout_3.addWidget(self.lineEdit_BlackCaptures, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.horizontalLayout_3.addWidget(self.widget_2, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.widget_3 = QtWidgets.QWidget(self.horizontalLayoutWidget_2)
        self.widget_3.setMinimumSize(QtCore.QSize(241, 209))
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
        self.WhitePlayerName.setText("")
        self.WhitePlayerName.setFrame(False)
        self.WhitePlayerName.setAlignment(QtCore.Qt.AlignCenter)
        self.WhitePlayerName.setReadOnly(True)
        self.WhitePlayerName.setObjectName("WhitePlayerName")
        self.verticalLayout_4.addWidget(self.WhitePlayerName, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.lineEdit_WhiteCaptures = QtWidgets.QLineEdit(self.verticalWidget_2)
        self.lineEdit_WhiteCaptures.setReadOnly(True)
        self.lineEdit_WhiteCaptures.setObjectName("lineEdit_WhiteCaptures")
        self.verticalLayout_4.addWidget(self.lineEdit_WhiteCaptures, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.horizontalLayout_3.addWidget(self.widget_3, 0, QtCore.Qt.AlignHCenter)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(170, 390, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 390, 75, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_SaveGame = QtWidgets.QPushButton(self.widget)
        self.pushButton_SaveGame.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.pushButton_SaveGame.setObjectName("pushButton_SaveGame")
        self.pushButton_Exit = QtWidgets.QPushButton(self.widget)
        self.pushButton_Exit.setGeometry(QtCore.QRect(410, 10, 81, 31))
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        self.plainTextEdit_Probs = QtWidgets.QPlainTextEdit(self.widget)
        self.plainTextEdit_Probs.setGeometry(QtCore.QRect(0, 430, 501, 300))
        self.plainTextEdit_Probs.setPlainText("")
        self.plainTextEdit_Probs.setObjectName("plainTextEdit_Probs")
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1454, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_StartGame.setText(_translate("MainWindow", "START"))
        self.lineEdit_2.setText(_translate("MainWindow", "BLACK"))
        self.BlackPlayerName.setStyleSheet(_translate("MainWindow", "\n"
"background-color: rgba(255, 255, 255, 0);"))
        self.BlackPlayerName.setPlaceholderText(_translate("MainWindow", "Black Player"))
        self.lineEdit_4.setText(_translate("MainWindow", "WHITE"))
        self.WhitePlayerName.setStyleSheet(_translate("MainWindow", "\n"
"background-color: rgba(255, 255, 255, 0);"))
        self.WhitePlayerName.setPlaceholderText(_translate("MainWindow", "White Player"))
        self.pushButton.setText(_translate("MainWindow", "PASS"))
        self.pushButton_2.setText(_translate("MainWindow", "RESIGN"))
        self.pushButton_SaveGame.setText(_translate("MainWindow", "Save Game"))
        self.pushButton_Exit.setText(_translate("MainWindow", "Exit"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
