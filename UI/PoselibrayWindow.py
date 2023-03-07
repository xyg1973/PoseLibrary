# -*- coding: utf-8 -*-
'''
Demonstrates how to create a QDockWidget with PySide2 for use in 3ds Max
'''
from PySide2.QtGui import QIcon
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import shiboken2
from pymxs import runtime as rt
import pymxs
import os


def make_cylinder():
    cyl = rt.Cylinder(radius=10, height=30)
    rt.redrawViews()

    return


class PyMaxDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('Pyside Qt  Dock Window')
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1055, 695)
        MainWindow.setStyleSheet("QMainWindow\n"
                                 "{\n"
                                 "background-color:rgb(55, 56, 60);\n"
                                 "\n"
                                 "border: 0px solid rgb(17, 17, 17);\n"
                                 "}    \n"
                                 "")
        #MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.Main_Widget = QtWidgets.QWidget(MainWindow)
        self.Main_Widget.setStyleSheet("QWidget{\n"
                                       "    background-color:rgba(10,225,225,0);\n"
                                       "    border-radius:0px;\n"
                                       "}")
        self.Main_Widget.setObjectName("Main_Widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Main_Widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(3, 0, 3, -1)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName("mainLayout")
        self.list_frame = QtWidgets.QFrame(self.Main_Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_frame.sizePolicy().hasHeightForWidth())
        self.list_frame.setSizePolicy(sizePolicy)
        self.list_frame.setStyleSheet("QFrame{\n"
                                      "background-color: transparent;\n"
                                      "\n"
                                      "}")
        self.list_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.list_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.list_frame.setObjectName("list_frame")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.list_frame)
        self.verticalLayout_7.setContentsMargins(6, 12, 6, 0)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_3 = QtWidgets.QPushButton(self.list_frame)
        self.pushButton_3.setStyleSheet("QPushButton {\n"
                                        "    background-color:transparent;\n"
                                        "    color: rgb(255, 255, 255);\n"
                                        "    border-style: outset;\n"
                                        "    border-width: 0px;\n"
                                        "    border-radius: 3px;\n"
                                        "    border-color: beige;\n"
                                        "\n"
                                        "    padding: 2px;\n"
                                        "    text-align:left\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgb(150, 150, 150);\n"
                                        "}\n"
                                        "QPushButton:pressed {\n"
                                        "    background-color:  rgb(210, 210, 210);\n"
                                        "    border-style: inset;\n"
                                        "}")
        self.pushButton_3.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_8.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.pushButton_17 = QtWidgets.QPushButton(self.list_frame)
        self.pushButton_17.setMinimumSize(QtCore.QSize(180, 0))
        self.pushButton_17.setStyleSheet("QPushButton {\n"
                                         "    background-color:transparent;\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "    border-style: outset;\n"
                                         "    border-width: 0px;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-color: beige;\n"
                                         "    padding: 2px;\n"
                                         "    text-align:left\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(150, 150, 150);\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background-color:  rgb(210, 210, 210);\n"
                                         "    border-style: inset;\n"
                                         "}")
        self.pushButton_17.setObjectName("pushButton_17")
        self.verticalLayout_13.addWidget(self.pushButton_17)
        self.pushButton_18 = QtWidgets.QPushButton(self.list_frame)
        self.pushButton_18.setStyleSheet("QPushButton {\n"
                                         "    background-color:transparent;\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "    border-style: outset;\n"
                                         "    border-width: 0px;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-color: beige;\n"
                                         "    padding: 2px;\n"
                                         "    text-align:left\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(150, 150, 150);\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background-color:  rgb(210, 210, 210);\n"
                                         "    border-style: inset;\n"
                                         "}")
        self.pushButton_18.setObjectName("pushButton_18")
        self.verticalLayout_13.addWidget(self.pushButton_18)
        self.verticalLayout_7.addLayout(self.verticalLayout_13)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(3, -1, -1, -1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.treeWidget = QtWidgets.QTreeWidget(self.list_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setStyleSheet("QTreeWidget\n"
                                      "{\n"
                                      "background-color: transparent;\n"
                                      "color:rgb(255, 255, 255);\n"
                                      "border: 0px solid rgb(17, 17, 17);\n"
                                      "}    \n"
                                      "QTreeWidget::item {\n"
                                      "    background-color:transparent;\n"
                                      "    color: rgb(255, 255, 255);\n"
                                      "    border-style: outset;\n"
                                      "    border-width: 0px;\n"
                                      "    border-radius: 3px;\n"
                                      "    border-color: beige;\n"
                                      "    padding: 2px;\n"
                                      "    text-align:left\n"
                                      "}\n"
                                      "QTreeWidget::item:hover {\n"
                                      "    background-color: rgb(150, 150, 150);\n"
                                      "}\n"
                                      "QTreeWidget::item:pressed {\n"
                                      "    background-color:  rgb(210, 210, 210);\n"
                                      "    border-style: inset;\n"
                                      "}\n"
                                      "\n"
                                      "")
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        self.verticalLayout_8.addWidget(self.treeWidget)
        self.verticalLayout_7.addLayout(self.verticalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(9, 0, 6, 0)
        self.horizontalLayout_7.setSpacing(3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.list_frame)
        self.lineEdit_2.setStyleSheet("QLineEdit{\n"
                                      "background-color: rgb(38, 39, 42);\n"
                                      "color:rgb(255, 255, 255);\n"
                                      "border-radius: 5px; \n"
                                      "border: 1px solid rgb(17, 17, 17);\n"
                                      "padding: 2px;\n"
                                      "}\n"
                                      "")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_7.addWidget(self.lineEdit_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        spacerItem1 = QtWidgets.QSpacerItem(122, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_7.addItem(spacerItem1)
        self.verticalLayout_7.setStretch(2, 1)
        self.mainLayout.addWidget(self.list_frame)
        self.library_frame = QtWidgets.QFrame(self.Main_Widget)
        self.library_frame.setStyleSheet("QFrame{\n"
                                         "    background-color:rgb(48, 49, 53);\n"
                                         "    border-radius:0px;\n"
                                         "}")
        self.library_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.library_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.library_frame.setObjectName("library_frame")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.library_frame)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_11.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.UI_Library = QtWidgets.QVBoxLayout()
        self.UI_Library.setContentsMargins(-1, 0, -1, -1)
        self.UI_Library.setObjectName("UI_Library")
        self.UI_Library_frame = QtWidgets.QFrame(self.library_frame)
        self.UI_Library_frame.setStyleSheet("")
        self.UI_Library_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UI_Library_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.UI_Library_frame.setObjectName("UI_Library_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.UI_Library_frame)
        self.verticalLayout_6.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(3, 3, 5, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.lineEdit = QtWidgets.QLineEdit(self.UI_Library_frame)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setStyleSheet("QLineEdit{\n"
                                    "background-color: rgb(38, 39, 42);\n"
                                    "color:rgb(255, 255, 255);\n"
                                    "border-radius: 5px; \n"
                                    "border: 1px solid rgb(17, 17, 17);\n"
                                    "padding: 2px;\n"
                                    "}\n"
                                    "")
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_4.addWidget(self.lineEdit)
        self.verticalLayout_9.addLayout(self.horizontalLayout_4)
        self.frame_2 = QtWidgets.QFrame(self.UI_Library_frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_10.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_2)
        self.scrollArea.setStyleSheet("QAbstractScrollArea\n"
                                      "{\n"
                                      "background-color: transparent;\n"
                                      "border: 0px solid rgb(17, 17, 17);\n"
                                      "}    \n"
                                      "\n"
                                      "QWidget#scrollAreaWidgetContents{\n"
                                      "background-color: transparent; /*or a colour*/\n"
                                      "}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 572, 646))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.frame_4)
        self.horizontalLayout_5.addLayout(self.formLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_10.addWidget(self.scrollArea)
        self.verticalLayout_9.addWidget(self.frame_2)
        self.verticalLayout_9.setStretch(1, 1)
        self.verticalLayout_6.addLayout(self.verticalLayout_9)
        self.UI_Library.addWidget(self.UI_Library_frame)
        self.horizontalLayout_2.addLayout(self.UI_Library)
        self.verticalLayout_11.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_11.addLayout(self.horizontalLayout)
        self.mainLayout.addWidget(self.library_frame)
        self.card_frame = QtWidgets.QFrame(self.Main_Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.card_frame.sizePolicy().hasHeightForWidth())
        self.card_frame.setSizePolicy(sizePolicy)
        self.card_frame.setStyleSheet("QFrame{\n"
                                      "    background-color:rgba(10,225,225,0);\n"
                                      "    border-radius:0px;\n"
                                      "}")
        self.card_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.card_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.card_frame.setObjectName("card_frame")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.card_frame)
        self.verticalLayout_12.setContentsMargins(6, 12, 6, 0)
        self.verticalLayout_12.setSpacing(3)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton = QtWidgets.QPushButton(self.card_frame)
        self.pushButton.setEnabled(False)
        self.pushButton.setStyleSheet("QPushButton {\n"
                                      "    background-color:transparent;\n"
                                      "    color: rgb(255, 255, 255);\n"
                                      "    border-style: outset;\n"
                                      "    border-width: 0px;\n"
                                      "    border-radius: 3px;\n"
                                      "    border-color: beige;\n"
                                      "    padding: 2px;\n"
                                      "    text-align:left\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb(150, 150, 150);\n"
                                      "}\n"
                                      "QPushButton:pressed {\n"
                                      "    background-color:  rgb(210, 210, 210);\n"
                                      "    border-style: inset;\n"
                                      "}\n"
                                      "\n"
                                      "")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_5.addWidget(self.pushButton)
        self.verticalLayout_12.addLayout(self.verticalLayout_5)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setContentsMargins(-1, 10, 6, 10)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.pushButton_15 = QtWidgets.QPushButton(self.card_frame)
        self.pushButton_15.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_15.setStyleSheet("QPushButton {\n"
                                         "    background-color:argb(10, 10, 10,40);\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "    border-style: outset;\n"
                                         "    border-width: 0px;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-color: beige;\n"
                                         "    padding: 2px;\n"
                                         "\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color:argb(10, 10, 10,80);\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background-color:  argb(10, 10, 10,150);\n"
                                         "    border-style: inset;\n"
                                         "}\n"
                                         "")
        self.pushButton_15.setText("")
        self.pushButton_15.setIconSize(QtCore.QSize(150, 150))
        self.pushButton_15.setObjectName("pushButton_15")
        self.verticalLayout_17.addWidget(self.pushButton_15)
        self.verticalLayout_12.addLayout(self.verticalLayout_17)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.pushButton_19 = QtWidgets.QPushButton(self.card_frame)
        self.pushButton_19.setEnabled(False)
        self.pushButton_19.setStyleSheet("QPushButton {\n"
                                         "    background-color:transparent;\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "    border-style: outset;\n"
                                         "    border-width: 0px;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-color: beige;\n"
                                         "    padding: 2px;\n"
                                         "    text-align:left\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(150, 150, 150);\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background-color:  rgb(210, 210, 210);\n"
                                         "    border-style: inset;\n"
                                         "}")
        self.pushButton_19.setObjectName("pushButton_19")
        self.verticalLayout_16.addWidget(self.pushButton_19)
        self.label = QtWidgets.QLabel(self.card_frame)
        self.label.setStyleSheet("QLabel{\n"
                                 "    background-color:transparent;\n"
                                 "    color:rgb(176, 176, 176);\n"
                                 "    border-style: outset;\n"
                                 "    border-width: 0px;\n"
                                 "    border-radius: 3px;\n"
                                 "    border-color: beige;\n"
                                 "    padding: 2px;\n"
                                 "    text-align:left\n"
                                 "}\n"
                                 "")
        self.label.setObjectName("label")
        self.verticalLayout_16.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.card_frame)
        self.label_2.setStyleSheet("QLabel{\n"
                                   "    background-color:transparent;\n"
                                   "    color:rgb(176, 176, 176);\n"
                                   "    border-style: outset;\n"
                                   "    border-width: 0px;\n"
                                   "    border-radius: 3px;\n"
                                   "    border-color: beige;\n"
                                   "    padding: 2px;\n"
                                   "    text-align:left\n"
                                   "}\n"
                                   "")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_16.addWidget(self.label_2)
        self.verticalLayout_12.addLayout(self.verticalLayout_16)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.pushButton_20 = QtWidgets.QPushButton(self.card_frame)
        self.pushButton_20.setEnabled(False)
        self.pushButton_20.setStyleSheet("QPushButton {\n"
                                         "    background-color:transparent;\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "    border-style: outset;\n"
                                         "    border-width: 0px;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-color: beige;\n"
                                         "    padding: 2px;\n"
                                         "    text-align:left\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(150, 150, 150);\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background-color:  rgb(210, 210, 210);\n"
                                         "    border-style: inset;\n"
                                         "}")
        self.pushButton_20.setObjectName("pushButton_20")
        self.verticalLayout_15.addWidget(self.pushButton_20)
        self.checkBox = QtWidgets.QCheckBox(self.card_frame)
        self.checkBox.setStyleSheet("QCheckBox{\n"
                                    "    background-color:transparent;\n"
                                    "    color:rgb(176, 176, 176);\n"
                                    "    border-style: outset;\n"
                                    "    border-width: 0px;\n"
                                    "    border-radius: 3px;\n"
                                    "    border-color: beige;\n"
                                    "    padding: 2px;\n"
                                    "    text-align:left\n"
                                    "}\n"
                                    "")
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_15.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.card_frame)
        self.checkBox_2.setStyleSheet("QCheckBox{\n"
                                      "    background-color:transparent;\n"
                                      "    color:rgb(176, 176, 176);\n"
                                      "    border-style: outset;\n"
                                      "    border-width: 0px;\n"
                                      "    border-radius: 3px;\n"
                                      "    border-color: beige;\n"
                                      "    padding: 2px;\n"
                                      "    text-align:left\n"
                                      "}\n"
                                      "")
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_15.addWidget(self.checkBox_2)
        self.pushButton_12 = QtWidgets.QPushButton(self.card_frame)
        self.pushButton_12.setStyleSheet("QPushButton {\n"
                                         "    background-color:transparent;\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "    border-style: outset;\n"
                                         "    border-width: 0px;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-color: beige;\n"
                                         "    padding: 2px;\n"
                                         "    text-align:left\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(150, 150, 150);\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background-color:  rgb(210, 210, 210);\n"
                                         "    border-style: inset;\n"
                                         "}")
        self.pushButton_12.setObjectName("pushButton_12")
        self.verticalLayout_15.addWidget(self.pushButton_12)
        self.horizontalSlider = QtWidgets.QSlider(self.card_frame)
        self.horizontalSlider.setMinimum(-100)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_15.addWidget(self.horizontalSlider)
        self.verticalLayout_12.addLayout(self.verticalLayout_15)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(6, 15, 6, 6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_11 = QtWidgets.QPushButton(self.card_frame)
        self.pushButton_11.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_11.setStyleSheet("QPushButton {\n"
                                         "    background-color:rgb(0, 114, 239);\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "    border-style: outset;\n"
                                         "    border-width: 0px;\n"
                                         "    border-radius: 3px;\n"
                                         "    border-color: beige;\n"
                                         "    padding: 2px;\n"
                                         "\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(50, 164, 239);\n"
                                         "}\n"
                                         "QPushButton:pressed {\n"
                                         "    background-color: rgb(100, 214, 239);\n"
                                         "    border-style: inset;\n"
                                         "}")
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_6.addWidget(self.pushButton_11)
        self.verticalLayout_12.addLayout(self.horizontalLayout_6)
        spacerItem3 = QtWidgets.QSpacerItem(220, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(220, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_12.addItem(spacerItem4)
        self.mainLayout.addWidget(self.card_frame)
        self.mainLayout.setStretch(0, 4)
        self.mainLayout.setStretch(1, 10)

        # 定义图片文件夹路径
        dir_path = 'H:/pycharm_max_work/poselibray/UI/icons'

        # 创建QTreeWidget对象
        self.tree_widget = QtWidgets.QTreeWidget()

        # 设置树形菜单的表头
        self.tree_widget.setHeaderLabels(["Images"])
        self.tree_widget.setHeaderHidden(True)
        # 遍历图片文件夹，生成树形菜单
        for root, dirs, files in os.walk(dir_path):
            # 添加文件夹节点
            if __name__ == '__main__':
                print("")
                #folder_item = QtWidgets.QTreeWidgetItem(self.tree_widget, [os.path.basename(root)])
                #folder_item.setIcon(0, QIcon("./bilibili-line.png"))
            # 遍历文件夹中的图片
                for file in files:
                    # 添加图片节点
                    img_item = QtWidgets.QTreeWidgetItem(self.tree_widget, [file])
                    img_item.setIcon(0, QIcon(os.path.join(root, file)))

        # 设置节点可折叠
        self.tree_widget.setItemsExpandable(True)

        # 添加信号槽，监听节点点击事件
        #tree_widget.itemClicked.connect(on_item_clicked)

        # 将树形菜单添加到界面上
        self.formLayout_2.addWidget(self.tree_widget)


        self.verticalLayout_2.addLayout(self.mainLayout)
        # MainWindow.setCentralWidget(self.Main_Widget)
        testwidget = QtWidgets.QWidget()
        testwidget.setLayout(self.verticalLayout_2)
        self.setWidget(testwidget)
        self.resize(1000, 600)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_3.setText(_translate("MainWindow", "项目1"))
        self.pushButton_17.setText(_translate("MainWindow", "  全部"))
        self.pushButton_18.setText(_translate("MainWindow", "  标签"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "New Column"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.topLevelItem(3).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.topLevelItem(3).child(0).setText(0, _translate("MainWindow", "New Subitem"))
        self.treeWidget.topLevelItem(3).child(1).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.topLevelItem(3).child(2).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.topLevelItem(3).child(3).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.topLevelItem(3).child(3).child(0).setText(0, _translate("MainWindow", "New Subitem"))
        self.treeWidget.topLevelItem(3).child(3).child(1).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.topLevelItem(3).child(3).child(2).setText(0, _translate("MainWindow", "New Item"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("MainWindow", "选择类型"))
        self.pushButton_19.setText(_translate("MainWindow", "文件信息:"))
        self.label.setText(_translate("MainWindow", "  TextLabel"))
        self.label_2.setText(_translate("MainWindow", "  TextLabel"))
        self.pushButton_20.setText(_translate("MainWindow", "应用设置:"))
        self.checkBox.setText(_translate("MainWindow", "绝对位置"))
        self.checkBox_2.setText(_translate("MainWindow", "当前时间插入"))
        self.pushButton_12.setText(_translate("MainWindow", "权重"))
        self.pushButton_11.setText(_translate("MainWindow", "应用"))


def main():
    # rt.resetMaxFile(rt.name('noPrompt'))
    # Cast the main window HWND to a QMainWindow for docking
    # First, get the QWidget corresponding to the Max windows HWND:
    main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())
    # Then cast it as a QMainWindow for docking purposes:
    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)
    w = PyMaxDockWidget(parent=main_window)
    w.setFloating(True)
    w.show()


if __name__ == '__main__':
    main()