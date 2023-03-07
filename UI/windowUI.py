# -*- coding: utf-8 -*-
import sys
import json
sys.path.append("H:/pycharm_max_work/poselibray")
from PySide2.QtGui import QIcon
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import shiboken2
from PySide2.QtCore import QTimer
from pymxs import runtime as rt
import pymxs
import gc
import os
from Tools import file
from  Tools import QTcommand
from UI import PoseWindow
from Maxcommand import pose as pose

#reload(PoseWindow)
PROJECT_PATH =""
PROJECT_NAME =""
SELECTITEMPATH = ""
LISTITEMPATH =""
JSONPATH = ""
pypath = os.getcwd()

QTcommand.pypath = pypath

# pypath ="H:\pycharm_maya_work\Design"
print("windowUI的路径是" + pypath)
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

reload_module('Tools.file')
reload_module('Tools.QTcommand')
reload_module('UI.PoseWindow')
reload_module('Maxcommand.pose')

class MainWindow(QtWidgets.QMainWindow):
    size_changed = QtCore.Signal(int, int)
    m_flag = False
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = PoseWindow.Ui_MainWindow()

        self.ui.setupUi(self)
        self.setWindowTitle("PoseLibrary")
        #隐藏window 抬头
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.handle_timeout)
        self._timer.setSingleShot(True)
        self.show()
        self.workflow()

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////

    def creat_contion(self):
        """
        创建连接
        :return:
        """
        self.ui.Btn_win_max.clicked.connect(self.restore_or_maximize_window)
        self.ui.Btn_win_close.clicked.connect(self.close)

        self.ui.treeWidget_2.itemClicked.connect(self.UpdataLibrary)
        self.ui.tableWidget.itemSelectionChanged.connect(self.UpdataCradData)  #单击事件
        #self.ui.tableWidget.itemDoubleClicked.connect(self.apply_pose)#双击事件
        self.ui.Btn_HomePagge.clicked.connect(self.Btn_HomePaggeEvent)
        self.ui.Btn_Creat.clicked.connect(self.CreatPose)
        self.ui.Btn_Apply.clicked.connect(self.ApplyPose)
        self.ui.pushButton_5.clicked.connect(self.creatProject)
        self.ui.Btn_Add.clicked.connect(self.AddFolder)
        self.ui.Btn_Expand.clicked.connect(self.Expandmin)
        self.ui.pushButton_3.clicked.connect(self.Expandmax)

    def Expandmin(self):
        self.ui.dockWidget.setVisible(False)
        self.ui.dockWidget_2.setVisible(False)
        self.ui.dockWidget_top.setVisible(False)
        self.ui.pushButton_3.setVisible(True)

    def Expandmax(self):
        self.ui.dockWidget.setVisible(True)
        self.ui.dockWidget_2.setVisible(True)
        self.ui.dockWidget_top.setVisible(True)
        self.ui.pushButton_3.setVisible(False)

    def AddFolder(self):
        global PROJECT_PATH
        if not self.ui.treeWidget_2.selectedItems():
            item = QtWidgets.QTreeWidgetItem(["未命名文件夹"])
            icon5 = QtGui.QIcon()
            icon5.addPixmap(QtGui.QPixmap(pypath + "\img/folder-dynamic-color.png"), QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
            item.setIcon(0, icon5)
            self.ui.treeWidget_2.insertTopLevelItems(0, [item])

            print("未选择Item")
        else:
            item = QTcommand.add_child(self.ui.treeWidget_2)
            icon5 = QtGui.QIcon()
            icon5.addPixmap(QtGui.QPixmap(pypath + "\img/folder-dynamic-color.png"), QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
            item.setIcon(0, icon5)
            print("xu")

    def creatProject(self):
        global PROJECT_NAME
        global PROJECT_PATH
        name = self.ui.lineEdit_2.text()
        if name ==[]:
            pass
        else:
            dialog = QtWidgets.QFileDialog(self, '选择文件夹', './')
            dialog.resize(300, 150)  # 设置窗口大小
            folder_path = dialog.getExistingDirectory()

            os.makedirs(folder_path+"\\"+name)#创建工程文件夹
            PROJECT_PATH = folder_path+"\\"+name
            PROJECT_NAME = name
            self.stepWindowUi()
            self.creat_contion()
            self.UpdataLibrary()

            self.ui.dockWidget.setVisible(True)
            self.ui.dockWidget_2.setVisible(True)
            self.ui.UI_Library_frame.setVisible(True)
            self.ui.dockWidget_top.setVisible(True)
            self.ui.frame_9.setVisible(False)
            print(PROJECT_PATH)
            print(PROJECT_NAME)

    def Btn_HomePaggeEvent(self):
        #设置item没有选中
        self.ui.treeWidget_2.clearSelection()
        #刷新表格
        QTcommand.updataLibraryItem(PROJECT_PATH,self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())

    def CreatPose(self):
        global PROJECT_PATH
        # pose.make_cylinder()
        name = self.UI_addpose_inputDialog()
        jsonname = name + ".json"
        print(PROJECT_PATH)
        filepath = PROJECT_PATH +"\\"+jsonname
        pngpath = PROJECT_PATH +"\\"+name+".png"
        open(filepath, 'w').close()
        posedata = pose.savePose()

        with open(filepath, 'w') as f:
            json.dump(posedata, f)

        pose.render_and_save(300,300,pngpath)
        QTcommand.updataLibraryItem(PROJECT_PATH,self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())
        return posedata

    def ApplyPose(self):
        global JSONPATH
        # 定位json路径
        path = JSONPATH
        print(path)
        # 读取数据
        with open(path, 'r') as f:
            posedata = json.load(f)
        #获取设置

        selectobj = pose.selectobj(posedata)
        pose.pastPose(posedata,selectobj)
        #pose.set_transform_keyframes(selectobj)
        #应用pose


    def UI_addpose_inputDialog(self):
        name,ok = QtWidgets.QInputDialog.getText(self,"name","name",QtWidgets.QLineEdit.Normal,"pose")
        if ok :
            return name

    def UpdataLibrary(self):
        global LISTITEMPATH

        def get_item_path(item):
            path = []
            while item:
                path.append(item.text(0))
                item = item.parent()
            return path[::-1]

        selected_items = self.ui.treeWidget_2.selectedItems()
        for item in selected_items:
            path = get_item_path(item)
            path = path[0].encode("utf-8").decode("unicode_escape")
            print(path)
            LISTITEMPATH = '/'.join(path)

        if not self.ui.treeWidget_2.selectedItems():
            QTcommand.updataLibraryItem(PROJECT_PATH, self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())
        else:
            QTcommand.updataLibraryItem(PROJECT_PATH+"//"+ unicode(LISTITEMPATH), self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())

        return LISTITEMPATH

    def UpdataCradData(self):
        """
        刷新预览图和文件信息
        :return:
        """
        #获取选中的ite
        global LISTITEMPATH
        global JSONPATH
        selected = self.ui.tableWidget.selectedIndexes()
        # print(selected)
        for item in selected:
            row = item.row()
            column = item.column()
        frame = self.ui.tableWidget.cellWidget(row, column)
        lineEdits = frame.findChildren(QtWidgets.QLineEdit)
        name = lineEdits[0].text()
        SELECTITEMPATH = PROJECT_PATH+"//"+LISTITEMPATH+"//"+name+".png"
        path = PROJECT_PATH+"//"+LISTITEMPATH+"//"+name+".json"
        print(SELECTITEMPATH,LISTITEMPATH)
        QTcommand.BtnSetIcons(self.ui.pushButton_4, SELECTITEMPATH)
        self.ui.pushButton_4.setIconSize(QtCore.QSize(200, 200))
        self.ui.Lbl_Name.setText("name: "+ name)
        self.ui.Lbl_ObjCount.setText(name + (" Objects"))
        #self.ui.Lbl_Path.setText("path: "+ path)
        JSONPATH =path

        if not self.ui.treeWidget_2.selectedItems():
            JSONPATH = PROJECT_PATH +"//"+name+".json"
        else:
            JSONPATH = path
        print(JSONPATH)
        return JSONPATH

    def workflow(self):
        if PROJECT_PATH =="":
            self.startWindwoUi()

        else:

            self.stepWindowUi()
            self.creat_contion()
            self.UpdataLibrary()

            self.ui.frame_9.setVisible(False)
            #创建目录
            pass
            # QTcommand.updataListItem(PROJECT_PATH, self.ui.treeWidget_2)
            # QTcommand.updataLibraryItem(PROJECT_PATH, self.ui.tableWidget,self.ui.centralwidget.frameGeometry().width())


    def startWindwoUi(self):
        self.ui.dockWidget.setVisible(False)
        self.ui.dockWidget_2.setVisible(False)
        self.ui.UI_Library_frame.setVisible(False)
        self.ui.dockWidget_top.setVisible(False)



    def stepWindowUi(self):
        # window.ui.statusbar.setVisible(False)
        #self.ui.statusbar.setFixedSize(600,5)
        self.ui.statusbar.setStyleSheet("QStatusBar {background: transparent;}"
                                "QStatusBar::item {"
                                "border: 1px solid red;"
                                "border-radius: 3px;"
                                "}")
        self.docktitle = QtWidgets.QWidget()
        self.docktitle_2 = QtWidgets.QWidget()
        self.docktitle_top = QtWidgets.QWidget()
        self.ui.dockWidget.setTitleBarWidget(self.docktitle)
        self.ui.dockWidget_2.setTitleBarWidget(self.docktitle_2)
        self.ui.dockWidget_top.setTitleBarWidget(self.docktitle_top)
        self.ui.pushButton_3.setVisible(False)
        self.ui.pushButton.setVisible(False)
        QTcommand.BtnSetIcons(self.ui.Btn_Menu, pypath+"\img//cube-iso-clay.png")
        print (pypath+"\img//cube-iso-clay.png")
        QTcommand.BtnSetIcons(self.ui.Btn_Add, pypath+"\img//new-folder-dynamic-color.png")
        QTcommand.BtnSetIcons(self.ui.Btn_Expand, pypath+"\img//figma-dynamic-clay.png")
        QTcommand.BtnSetIcons(self.ui.Btn_Creat, pypath+"\img//plus-dynamic-clay.png")
        QTcommand.BtnSetIcons(self.ui.pushButton_4, pypath+"\img//picture-dynamic-clay.png")
        QTcommand.BtnSetIcons(self.ui.pushButton_3, pypath+"\img//figma-dynamic-clay.png")

        self.ui.dockWidget.widget().setMinimumSize(QtCore.QSize(120, 150))
        self.ui.dockWidget.widget().setMaximumSize(QtCore.QSize(200, 150000))
        # window.ui.dockWidget_2.widget().setMinimumSize(QtCore.QSize(150, 400))
        self.ui.dockWidget_2.widget().setMaximumSize(QtCore.QSize(400, 150000))

        self.ui.Lbl_Folder.setText (PROJECT_NAME)
        self.ui.treeWidget_2.clear()
        #print(self.ui.centralwidget.frameGeometry().width())
        # QtWidgets.QMainWindow.centralWidget()

        #设置选中没有虚线
        self.ui.Btn_HomePagge.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Add.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Menu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Expand.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_win_max.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.treeWidget_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Creat.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.pushButton_4.setFocusPolicy(QtCore.Qt.NoFocus)
        print("设置UI样式")

    def handle_timeout(self):
        self._blocked = False

    def resizeEvent(self, event):
        if not self._timer.isActive():
            self.size_changed.emit(event.size().width(), event.size().height())
            self._blocked = True
            self._timer.start(500) # 屏蔽信号的时间，单位毫秒
        elif not self._blocked:
            self._timer.stop()
            self._timer.start(500)
            self._blocked = True
        super(MainWindow, self).resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() ==QtCore.Qt.LeftButton and self.isMaximized() ==False:
            self.m_flag = True
            self.m_Position = event.globalPos() -self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)
            mouse_event.accept()
    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()

        else:
            self.showMaximized()

    def evenrfilter(self):
        self.installEventFilter(self)

def main():
    global  PROJECT_PATH
    global  LISTITEMPATH
    # rt.resetMaxFile(rt.name('noPrompt'))
    # Cast the main window HWND to a QMainWindow for docking
    # First, get the QWidget corresponding to the Max windows HWND:
    main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())
    # Then cast it as a QMainWindow for docking purposes:
    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)
    window = MainWindow(main_window)
    path = PROJECT_PATH+"//"+LISTITEMPATH
    def itemsort():
        # time.sleep(0.25)
        window.UpdataLibrary()


    def eventItemSort(w, h):
        QTimer.singleShot(250, itemsort)
        print("yes yes yes")

        gc.collect()  # python内置清除内存函数

    # 创建事件信号
    size_changed_signal =window.size_changed

    # 给信号绑定事件
    size_changed_signal.connect(eventItemSort)



    window.show()
    return window

def test():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    return window

if __name__ == "__main__":
    #pycharme run code///////////////////////////////////
    window = test()
    #/////////////////////////////
    #window = test()


    #QTcommand.itemsort(window.ui.tableWidget, AllItemFrame)



    # def itemsort(table=window.ui.tableWidget, allitem=AllItemFrame):
    #     # time.sleep(0.25)
    #     QTcommand.itemsort(table, allitem)


    # def eventItemSort(w, h):
    #     QTimer.singleShot(100, itemsort)
        # print("yes yes yes")

        #gc.collect()  # python内置清除内存函数

    # # 创建事件信号
    # size_changed_signal =window.size_changed
    #
    # # 给信号绑定事件
    # size_changed_signal.connect(eventItemSort)

    sys.exit(app.exec_())


