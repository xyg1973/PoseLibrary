# -*- coding: utf-8 -*-

import sys
import json
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import shiboken2
from pymxs import runtime as rt
import pymxs
import os
import time
def reload_module(module_name):
    # 检查模块是否已经导入
    if module_name in sys.modules:
        # 如果已经导入，则重新加载
        try:
            # Python 2
            reload(sys.modules[module_name])
        except NameError:
            # Python 3
            import importlib
            importlib.reload(sys.modules[module_name])
    else:
        # 如果没有导入，则正常导入
        __import__(module_name)
try:
    from PoseLibrary.temp.bath_tool import bath_tool as bath_tool

    reload_module('PoseLibrary.temp.bath_tool.bath_tool')

except:
    pass

def getfile(path,filetype):
    """
    给定路径和文件类型，返回路径下类型所有文件的路径
    :param path:
    :param flietype:
    :return: typefile path
    """

    path= u"{}".format(path)
    filetype = filetype
    filelist = []
    #处理打开library窗口没有刷新文件的问题
    if path == None:
        return filelist

    # print(path)
    # 获取路径下的png文件列表
    allfile = os.listdir(path)                    #获取item的路径下的文件和文件夹                               #定义变量存储.json文件
    for i in allfile :
        if i.rfind(filetype)!=-1:         #字符串从右边开始查找包含“.json”的文件，如果没有找到返回-1，如果不等于-1表示这个文件是json文件
            filelist.append(path+"/"+i)
        else:
            pass
    return filelist

def getfileName(path):
    """

    :param path:
    :return: filename
    """
    (file,ext) = os.path.splitext(path)
    (pathA,filename) = os.path.split(path)
    count = len(filename)-len(ext)
    filename = filename[0:count]
    return filename

class MainWindow(QtWidgets.QMainWindow):

    size_changed = QtCore.Signal(int, int)
    m_flag = False
    eventlist = []
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = bath_tool.Ui_mainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("SN_Anim_Batch_Tool")

        self.docktitle = QtWidgets.QWidget()
        self.docktitle_2 = QtWidgets.QWidget()
        self.ui.dockWidget.setTitleBarWidget(self.docktitle)
        self.ui.dockWidget_2.setTitleBarWidget(self.docktitle_2)
        # self.ui.dockWidget_2.setMinimumSize(QtCore.QSize(480, 660))
        self.ui.dockWidget_2.setVisible(False)
        self.ui.progressBar.setVisible(False)

        self.setStyleSheet("QMainWindow#MainWindow\n"
"{\n"
"background-color:rgb(200, 200, 200);\n"
"}    \n"
"")
        self.creat_contion()
    def creat_contion(self):
        # self.ui.menu_2.clicked.connect(self.showlogUI)
        # self.ui.menu_2.actions(self.showlogUI)
        self.ui.BtnA_newSkin.clicked.connect(self.clicked_BtnA_newSkin)
        self.ui.BtnA_max_path.clicked.connect(self.clicked_BtnA_max_path)
        self.ui.BtnA_svae_path.clicked.connect(self.clicked_BtnA_svae_path)
        self.ui.BtnA_RefreshList.clicked.connect(self.UpdataListA)
        self.ui.BtnA_Apply.clicked.connect(self.ApplyA)
        # self.ui.LEdit_max_path.u
        self.ui.treeWidgetA.setColumnWidth(0,30)
        self.ui.treeWidgetA.setColumnWidth(1, 200)
        self.ui.treeWidgetA.setColumnWidth(2, 600)
        self.ui.treeWidgetA.clear()
        pass

    def showlogUI(self):
        self.ui.dockWidget_2.setVisible(True)

    def dialog_getMaxFilePath(self):

        self.dialogmaxpath = QtWidgets.QFileDialog()
        # self.dialogmaxpath.setGeometry(QtCore.QRect(0, 0, 753, 753))
        # self.dialogmaxpath.setBaseSize(QtCore.QSize(500,500))
        folder_path,_= self.dialogmaxpath.getOpenFileName(self, '选择新的skin文件', 'c:\\',"Max files (*.max *.Max *.MAX)")

        # folder_path = myfileDialog.getOpenFileName(type=".max")
        # folder_path = myfileDialog.getExistingDirectory()
        return folder_path

    def dialog_getMaxFileDir(self):
        self.dialogFileDir = QtWidgets.QFileDialog()
        # self.dialogmaxpath.setGeometry(QtCore.QRect(0, 0, 753, 753))
        # self.dialogmaxpath.setBaseSize(QtCore.QSize(500,500))
        folder_path = self.dialogFileDir.getExistingDirectory(self, '选择max目录', 'c:\\' )

        # folder_path = myfileDialog.getOpenFileName(type=".max")
        # folder_path = myfileDialog.getExistingDirectory()
        return folder_path
    def dialog_getMaxFileSaveDir(self):
        self.dialogFileDir = QtWidgets.QFileDialog()
        # self.dialogmaxpath.setGeometry(QtCore.QRect(0, 0, 753, 753))
        # self.dialogmaxpath.setBaseSize(QtCore.QSize(500,500))
        folder_path = self.dialogFileDir.getExistingDirectory(self, '选择保存路径', 'c:\\' )

        # folder_path = myfileDialog.getOpenFileName(type=".max")
        # folder_path = myfileDialog.getExistingDirectory()
        return folder_path

    def clicked_BtnA_newSkin(self):
        folder_path = self.dialog_getMaxFilePath()
        print(folder_path)
        self.ui.LEdit_newSkin.setText(folder_path)

    def clicked_BtnA_max_path(self):
        folder_path = self.dialog_getMaxFileDir()
        if folder_path!="":
            print(folder_path)
            self.ui.LEdit_max_path.setText(folder_path)
            self.UpdataListA()
        else:
            print("文件为空")
    def clicked_BtnA_svae_path(self):
        folder_path = self.dialog_getMaxFileSaveDir()
        print(folder_path)
        self.ui.LEdit_svae_path.setText(folder_path)

    def UpdataListA(self):
        self.ui.treeWidgetA.clear()
        folder_path = self.ui.LEdit_max_path.text()
        self.UpdataListA_do(self.ui.treeWidgetA,folder_path)
    def UpdataListA_do(self,treeWidget,folder_path):
        treeWidget.clear()
        filelist = getfile(folder_path,".max")
        count = 1
        for path in filelist:

            item = QtWidgets.QTreeWidgetItem(treeWidget)
            item.setText(0,str(count))
            item.setTextAlignment(0,QtCore.Qt.AlignCenter)
            item.setText(1, getfileName(path))
            item.setText(2, path)
            filetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)) )
            item.setText(3, str(filetime))
            treeWidget.addTopLevelItem(item)
            count +=1
    def ApplyA(self):

        selectitems =self.ui.treeWidgetA.selectedItems()
        for item in selectitems:
            path = item.text(2)

            # print(item.text(2))
            try:
                rt.loadMaxFile(path,quiet=True)
                savepath = "C:/Users/chichungwu/Documents/SN AnimTool/"+item.text(1)+".bip"
                objA = rt.getNodeByName('Bip001')
                rt.biped.saveBipFile(objA.controller, savepath)

                print(savepath)
            except:
                print("读取文件错误")

        print("处理完成")

def main():

    # rt.resetMaxFile(rt.name('noPrompt'))
    # Cast the main window HWND to a QMainWindow for docking
    # First, get the QWidget corresponding to the Max windows HWND:
    main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())
    # Then cast it as a QMainWindow for docking purposes:
    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)
    window = MainWindow(main_window)
    window.show()