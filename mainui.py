# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.btn_input = QtWidgets.QPushButton(self.groupBox)
        self.btn_input.setMinimumSize(QtCore.QSize(50, 40))
        self.btn_input.setObjectName("btn_input")
        self.gridLayout.addWidget(self.btn_input, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_output = QtWidgets.QPushButton(self.groupBox)
        self.btn_output.setMinimumSize(QtCore.QSize(50, 50))
        self.btn_output.setObjectName("btn_output")
        self.gridLayout_2.addWidget(self.btn_output, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.verticalLayout.addWidget(self.groupBox_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "unpack_plist"))
        self.groupBox.setTitle(_translate("MainWindow", "编辑区"))
        self.label.setText(_translate("MainWindow", "请选择png文件："))
        self.btn_input.setText(_translate("MainWindow", "选择"))
        self.btn_output.setText(_translate("MainWindow", "开始生成"))
        self.groupBox_2.setTitle(_translate("MainWindow", "输出"))

    # 选择文件
    def choose_png_file(self):
        try:
            choose = QtWidgets.QFileDialog.getOpenFileName(None, '选择文件', '', 'Excel files(*.png)')
            if choose:
                self.lineEdit.setText(choose[0])
                self.outputWritten("选择的文件为：{}\n".format(self.lineEdit.text()))
        except Exception as e:
            self.outputWritten('{}\n'.format(e))

    # 在控制台中写入信息
    def outputWritten(self, text=None):
        # 获取文本框中文本的游标
        cursor = self.textEdit.textCursor()
        # 将游标位置移动到当前文本的结束处
        cursor.movePosition(QtGui.QTextCursor.End)
        # 写入文本
        cursor.insertText(text)
        # 设置文本的游标为创建了cursor
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()