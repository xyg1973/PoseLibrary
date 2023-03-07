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


class PyMaxDockWidget(QtWidgets.QMainWindow):
    size_changed = QtCore.Signal(int, int)
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('PoseLibray')
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.handle_timeout)
        self._timer.setSingleShot(True)



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
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
        self.MainLayout = QtWidgets.QHBoxLayout()
        self.MainLayout.setContentsMargins(3, 0, 3, -1)
        self.MainLayout.setSpacing(0)
        self.MainLayout.setObjectName("MainLayout")

        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents_2 = QtWidgets.QWidget(self.dockWidget)
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")

        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_7.setContentsMargins(6, 12, 6, 0)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.MainLayout.addWidget(self.dockWidget)






        self.Library_Frame = QtWidgets.QFrame(self.Main_Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Library_Frame.sizePolicy().hasHeightForWidth())
        self.Library_Frame.setSizePolicy(sizePolicy)
        self.Library_Frame.setStyleSheet("QFrame{\n"
"    background-color: transparent;\n"
"    border-radius:0px;\n"
"}")
        self.Library_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Library_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Library_Frame.setObjectName("Library_Frame")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.Library_Frame)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.MainLayout.addWidget(self.Library_Frame)



#         self.Card_Frame = QtWidgets.QFrame(self.Main_Widget)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.Card_Frame.sizePolicy().hasHeightForWidth())
#         self.Card_Frame.setSizePolicy(sizePolicy)
#         self.Card_Frame.setStyleSheet("QFrame{\n"
# "    background-color:rgba(10,225,225,0);\n"
# "    border-radius:0px;\n"
# "}")
#         self.Card_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.Card_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.Card_Frame.setObjectName("Card_Frame")
#         self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.Card_Frame)
#         self.verticalLayout_12.setContentsMargins(6, 12, 6, 0)
#         self.verticalLayout_12.setSpacing(3)
#         self.verticalLayout_12.setObjectName("verticalLayout_12")
#         self.MainLayout.addWidget(self.Card_Frame)
        self.MainLayout.setStretch(0, 4)
        self.MainLayout.setStretch(1, 10)
        self.MainLayout.setStretch(2, 4)
        self.verticalLayout_2.addLayout(self.MainLayout)
        #MainWindow.setCentralWidget(self.Main_Widget)


        self.testwidget = QtWidgets.QWidget()
        self.testwidget.setLayout(self.verticalLayout_2)
        #self.setWidget(testwidget)
        #self.resize(600, 600)

        self.setCentralWidget(self.testwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PoseLibray"))


    def handle_timeout(self):
        self._blocked = False

    def resizeEvent(self, event):
        if not self._timer.isActive():
            self.size_changed.emit(event.size().width(), event.size().height())
            self._blocked = True
            self._timer.start(2) # 屏蔽信号的时间，单位毫秒
        elif not self._blocked:
            self._timer.stop()
            self._timer.start(2)
            self._blocked = True
        super(PyMaxDockWidget, self).resizeEvent(event)
def main():
    # rt.resetMaxFile(rt.name('noPrompt'))
    # Cast the main window HWND to a QMainWindow for docking
    # First, get the QWidget corresponding to the Max windows HWND:
    main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())
    # Then cast it as a QMainWindow for docking purposes:
    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)
    poselibrayDockWidget = PyMaxDockWidget(parent=main_window)
    #poselibrayDockWidget.setFloating(True)
    poselibrayDockWidget.show()
    return poselibrayDockWidget

if __name__ == '__main__':
    main()