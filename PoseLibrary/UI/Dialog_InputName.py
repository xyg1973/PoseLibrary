# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_InputName.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Dialog_InputName(QtWidgets.QInputDialog):
    def __init__(self, parent=None):
        self.setupUi(self)
    def setupUi(self, Dialog_InputName):
        Dialog_InputName.setObjectName("Dialog_InputName")
        Dialog_InputName.resize(338, 178)
        Dialog_InputName.setMinimumSize(QtCore.QSize(338, 178))
        Dialog_InputName.setMaximumSize(QtCore.QSize(338, 178))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_InputName)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_10 = QtWidgets.QFrame(Dialog_InputName)
        self.frame_10.setMinimumSize(QtCore.QSize(320, 160))
        self.frame_10.setStyleSheet("QFrame#frame_10{\n"
"    background-color:rgb(60, 60, 60);\n"
"    border-radius:10px;\n"
"}\n"
"")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_7.setContentsMargins(23, 23, 23, 23)
        self.verticalLayout_7.setSpacing(15)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.frame_10)
        self.label_3.setStyleSheet("QLabel{\n"
"    background-color:transparent;\n"
"    color:rgb(225, 225, 225);\n"
"    border-width: 0px;\n"
"    border-radius: 3px;\n"
"    border-color: beige;\n"
"    padding: 2px;\n"
"    text-align:left\n"
"}\n"
"")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_10)
        self.lineEdit_2.setStyleSheet("QLineEdit{\n"
"background-color:rgb(42, 42, 42);\n"
"color:rgb(255, 255, 255);\n"
"border-radius: 5px; \n"
"border: 1px solid rgb(25, 25, 25);\n"
"padding: 2px;\n"
"}\n"
"")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_15.addWidget(self.lineEdit_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_15)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame_10)
        self.buttonBox.setMinimumSize(QtCore.QSize(0, 30))
        self.buttonBox.setStyleSheet("QPushButton {\n"
"    background-color:rgb(40, 105, 254);\n"
"    color: rgb(255, 255, 255);\n"
"    border-width: 0px;\n"
"    border-radius: 3px;\n"
"    border-color: beige;\n"
"    padding: 2px;\n"
"\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:rgb(14, 59, 229);\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(1, 33, 154);\n"
"    border-style: inset;\n"
"}\n"
"\n"
"")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_7.addWidget(self.buttonBox)
        self.verticalLayout.addWidget(self.frame_10)

        self.retranslateUi(Dialog_InputName)
        self.buttonBox.accepted.connect(Dialog_InputName.accept)
        self.buttonBox.rejected.connect(Dialog_InputName.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_InputName)

    def retranslateUi(self, Dialog_InputName):
        _translate = QtCore.QCoreApplication.translate
        Dialog_InputName.setWindowTitle(_translate("Dialog_InputName", "输入名称"))
        self.label_3.setText(_translate("Dialog_InputName", "输入名称"))
