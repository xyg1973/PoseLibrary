# -*- coding: utf-8 -*-

import sys
import json
# sys.path.append("H:/pycharm_max_work/poselibray")
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
# from PySide2 import shiboken2
from PySide2.QtCore import QTimer
# from pymxs import runtime as rt
# import pymxs
import gc
import os
from PoseLibrary.UI import PoseWindow as PoseWindow
from PoseLibrary.Tools import file as file
from PoseLibrary.Tools import QTcommand as QTcommand
from PoseLibrary.UI import PoseWindow as PoseWindow
from PoseLibrary.Maxcommand import pose as pose
from PoseLibrary.Maxcommand import cmds as cmds
from PoseLibrary.Maxcommand import render as render
from PoseLibrary.Maxcommand import anim as anim
#
#reload(PoseWindow)
PROJECT_PATH =""
PROJECT_NAME =""
SELECTITEMPATH = ""
LISTITEMPATH =""
CellPath = ""
CellRelativePath = ""
JSONPATH = ""
pypath = ""



rightMenuStyle = """
QMenu {
    /* 半透明效果 */
    background-color: rgb(80, 80, 80,);
    border: none;
    border-radius: 5px;
}

QMenu::item {
    border-radius: 5px;
    /* 这个距离很麻烦需要根据菜单的长度和图标等因素微调 */
    padding: 8px 48px 8px 30px; /* 36px是文字距离左侧距离*/
    background-color: transparent;
}

/* 鼠标悬停和按下效果 */
QMenu::item:selected {
    border-radius: 0px;
    /* 半透明效果 */
    background-color: rgb(52, 95, 251);
}

/* 禁用效果 */
QMenu::item:disabled {
    background-color: transparent;
}

/* 图标距离左侧距离 */
QMenu::icon {
    left: 15px;
}

/* 分割线效果 */
QMenu::separator {
    height: 1px;
    background-color: rgb(60, 60, 60);
}
"""
# pypath ="H:\pycharm_maya_work\Design"
# print("windowUI的路径是" + pypath)
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
    from PoseLibrary.Tools import file as file
    from PoseLibrary.Tools import QTcommand as QTcommand
    from PoseLibrary.UI import PoseWindow as PoseWindow
    from PoseLibrary.Maxcommand import pose as pose
    from PoseLibrary.Maxcommand import cmds as cmds
    from PoseLibrary.Maxcommand import render as render
    from PoseLibrary.Maxcommand import anim as anim



    reload_module('PoseLibrary.UI.PoseWindow')
    reload_module('PoseLibrary.Tools.file')
    reload_module('PoseLibrary.Tools.QTcommand')
    reload_module('PoseLibrary.Maxcommand.pose')
    reload_module('PoseLibrary.Maxcommand.cmds')
    reload_module('PoseLibrary.Maxcommand.render')
    reload_module('PoseLibrary.Maxcommand.anim')
    QTcommand.pypath = pypath
    print(QTcommand.pypath)

    # reload_module('threading')
except:
    pass


class RenameDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.lineedit = QtWidgets.QLineEdit()
        layout.addWidget(self.lineedit)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def textValue(self):
        return self.lineedit.text()


class MainWindow(QtWidgets.QMainWindow):

    size_changed = QtCore.Signal(int, int)
    m_flag = False
    eventlist = []
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = PoseWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.frame_11.setVisible(False)
        self.setWindowTitle("PoseLibrary")
        self.ui.treeWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget_2.installEventFilter(self)
        self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableWidget.installEventFilter(self)
        self.ui.dockWidget_down.setVisible(False)
        self.ui.dockWidget_top.setVisible(False)
        self.ui.progressBar.setVisible(False)
        self.ui.progressBar.setTextVisible(False)

        #事件过滤器

        # self.Btn_Project.installEventFilter(self)
        #隐藏window 抬头
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.handle_timeout)
        self._timer.setSingleShot(True)
        self.size_changed.connect(self.eventItemSort)
        self.resize(1000, 500)
        self.workflow()
        self.creat_contion()

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////


    def creat_contion(self):
        """
        创建连接
        :return:
        """
        self.ui.Btn_win_max.clicked.connect(self.restore_or_maximize_window)
        self.ui.Btn_win_close.clicked.connect(self.close)
        self.ui.treeWidget_2.itemClicked.connect(self.Click_Treeweiget)
        self.ui.tableWidget.itemSelectionChanged.connect(self.UpdataCradData)  #单击事件
        self.ui.tableWidget.doubleClicked.connect(self.selectPose)#双击事件
        self.ui.Btn_HomePagge.clicked.connect(self.Btn_HomePaggeEvent)
        self.ui.Btn_Creat.clicked.connect(self.CreatPose)
        self.ui.Btn_Apply.clicked.connect(self.ApplyPose)
        self.ui.Btn_Apply2.clicked.connect(self.ApplyPose)
        self.ui.pushButton_5.clicked.connect(self.creatProject)
        self.ui.Btn_Add.clicked.connect(self.AddFolder)
        self.ui.Btn_Expand.clicked.connect(self.Expandmin)
        self.ui.pushButton_3.clicked.connect(self.Expandmax)
        self.ui.pushButton_7.clicked.connect(self.CreatPose)
        self.ui.treeWidget_2.customContextMenuRequested.connect(self.TreeWeiget_rightMenuShow)
        self.ui.tableWidget.customContextMenuRequested.connect(self.TableWeiget_rightMenuShow)
        self.ui.horizontalSlider.valueChanged.connect(self.resize_TableItem)
        self.ui.Btn_Menu.clicked.connect(self.Btn_MenuShow)
        self.ui.Btn_Menu_2.clicked.connect(self.Btn_MenuShow)
        self.ui.Btn_PathTip.clicked.connect(self.UpdataLibrary)
        self.ui.Btn_Project.clicked.connect(self.Btn_Project_rightMenuShow)
        self.ui.Btn_Creat_Anim.clicked.connect(self.CreatAnim)

    def resize_TableItem(self):
        current_value = self.ui.horizontalSlider.value()
        minimum = self.ui.horizontalSlider.minimum()
        maximum = self.ui.horizontalSlider.maximum()
        normalized_value = (float(current_value) - float(minimum)) / (float(maximum) - float(minimum))
        QTcommand.itemWidth = 60 * ((normalized_value + 0.5) * 3)
        if self.ui.frame_2.isVisible():
            self.UpdataLibrary()

    # def Menu_rightMenuShow(self):
    def Btn_MenuShow(self):
        global PROJECT_PATH
        try:
            clikeMenu = QtWidgets.QMenu(self.ui.Btn_Menu)
            LibraryACtion = clikeMenu.addAction(u"资源库")
            FileACtion = clikeMenu.addAction(u"文件")
            HelpACtion = clikeMenu.addAction(u"帮助")
            SettingACtion = clikeMenu.addAction(u"偏好设置")
            UpdateACtion = clikeMenu.addAction(u"检查更新")
            AboutACtion = clikeMenu.addAction(u"关于")
            ExitACtion = clikeMenu.addAction(u"退出")
            action = clikeMenu.exec_(QtGui.QCursor.pos())
            if action == LibraryACtion:
                pass
            elif action == FileACtion:
                pass
            elif action == HelpACtion:
                pass
            elif action == SettingACtion:
                pass
            elif action == UpdateACtion:
                pass
            elif action == ExitACtion:
                pass
        except Exception as e:
            pass


            # print(e)
    def open_file_dialog(self):
        myfileDialog = QtWidgets.QFileDialog(self,'选择文件夹', './')
        myfileDialog .resize(300, 150)  # 设置窗口大小
        folder_path = myfileDialog.getExistingDirectory()
        return folder_path
    def myfileDialog(self):
        self.ui.myfileDialog = QtWidgets.QFileDialog(self,'选择文件夹', './')

        return self.ui.myfileDialog
    def Btn_Project_rightMenuShow(self):
        global PROJECT_PATH
        my_documents_path = os.path.expanduser('~/Documents')
        configfile = my_documents_path + "\poselibrary\poselibrary.txt"


        rightMenu = QtWidgets.QMenu(self.ui.Btn_Project)
        removeProjectAction = rightMenu.addAction(u"移除资源库")
        openProjectAction = rightMenu.addAction(u"打开其他资源库")
        action = rightMenu.exec_(QtGui.QCursor.pos())
        if action == removeProjectAction:
            # 配置文件
            data = None
            with open(configfile, 'w') as f:
                json.dump(data, f)
            PROJECT_PATH = ""
            self.workflow()
            self.size_changed.connect(self.eventItemSort)

            #删除清空配置文件
            pass
        elif action == openProjectAction:
            self.size_changed.disconnect(self.eventItemSort)
            self.creatProject()
            QTcommand.updataListItem(PROJECT_PATH, self.ui.treeWidget_2)
            self.size_changed.connect(self.eventItemSort)




    def TableWeiget_rightMenuShow(self):
        global rightMenuStyle
        global PROJECT_PATH
        global JSONPATH
        try:
            rightMenu = QtWidgets.QMenu(self.ui.tableWidget)
            self.setStyleSheet(rightMenuStyle)
            addPoseAction = rightMenu.addAction(u"添加pose")
            addAnimAction = rightMenu.addAction(u"添加Anim")
            selectObjAction =  rightMenu.addAction(u"选择物体")
            resPoseAction = rightMenu.addAction(u"刷新pose")

            renameAction =  rightMenu.addAction(u"重命名")
            removeAction = rightMenu.addAction(u"删除")

            action = rightMenu.exec_(QtGui.QCursor.pos())
            if action == removeAction:
                path = self.getCellPath()
                os.remove(path+".png")
                os.remove(path + ".json")
                self.UpdataLibrary()

            elif action == selectObjAction:

                path = JSONPATH
                # 读取数据
                with open(path, 'r') as f:
                    posedata = json.load(f)
                # 获取设置

                selectobj = cmds.selectobj(posedata)


            elif action == resPoseAction:
                self.resetPose()
                data = anim.saveAnim()
                selectobj = cmds.ls()
                # selectobj = cmds.selectobj(posedata)
                count = 2
                # print(data)
                self.ui.progressBar.setVisible(True)

                anim.pastAnim(data,selectobj,self.ui.progressBar)
                self.ui.progressBar.setVisible(False)
                print("完成")

            elif action == addPoseAction:
                self.CreatPose()
            elif action == renameAction:

                self.TableWeiget_reanameItem()


        except Exception as e:
            pass
            # print(e)
    def TreeWeiget_renameItem(self):

        def onItemChanged(item, column):
            self.ui.treeWidget_2.closePersistentEditor(item, column)
        path = self.getCellPath()
        parent_path = os.path.dirname(path)
        # print(path)

        selectItem = self.ui.treeWidget_2.selectedItems()[0]
        row = self.ui.treeWidget_2.indexOfTopLevelItem(selectItem)
        self.ui.treeWidget_2.openPersistentEditor(selectItem, 0 )

        def onItemChanged(item=selectItem):
            name = item.text(0)
            self.ui.treeWidget_2.closePersistentEditor(item,0)
            new_path = parent_path+"//"+name
            new_path = u'{}'.format(new_path)
            # print(new_path)
            # print(path)
            try:
                os.rename(path, new_path)
            except:
                pass

            return (name)



        # self.ui.treeWidget_2.closePersistentEditor(selectItem, 0)
        self.ui.treeWidget_2.itemChanged.connect(onItemChanged)
    def TreeWeiget_rightMenuShow(self):
        global PROJECT_PATH


        try:
            rightMenu = QtWidgets.QMenu(self.ui.treeWidget_2)
            addChildAction= rightMenu.addAction(u"添加子文件夹")
            renameAction = rightMenu.addAction(u"重命名")
            removeAction = rightMenu.addAction(u"删除")

            # copyAction = rightMenu.addAction(u"复制")
            action = rightMenu.exec_(QtGui.QCursor.pos())
            if action == removeAction:
                for item in self.ui.treeWidget_2.selectedItems():
                    index = self.ui.treeWidget_2.indexOfTopLevelItem(item)
                    itempath = QTcommand.get_item_path(self.ui.treeWidget_2)
                    itempath = PROJECT_PATH+"//"+itempath
                    file.remove_dir(itempath)
                    if index != -1:
                        self.ui.treeWidget_2.takeTopLevelItem (index)
                        self.UpdataLibrary()
                    else:
                        parent = item.parent()
                        parent.removeChild(item)
                        self.UpdataLibrary()

            elif action == addChildAction:
                for item in self.ui.treeWidget_2.selectedItems():
                    index = self.ui.treeWidget_2.indexOfTopLevelItem(item)
                    itempath = QTcommand.get_item_name(item)
                    folder_name = "folder"
                    if index != -1:


                        # 获取要创建的文件夹路径
                        folder_path = PROJECT_PATH + "//"+itempath+"//" + folder_name
                        folder_path = file.create_folder(folder_path)
                        folder_name = os.path.basename(folder_path)

                        #创建item
                        item = QTcommand.add_child(self.ui.treeWidget_2, name=folder_name)
                        icon5 = QtGui.QIcon()
                        icon5.addPixmap(QtGui.QPixmap(pypath + "\img/folder-dynamic-color.png"), QtGui.QIcon.Normal,
                                        QtGui.QIcon.Off)
                        item.setIcon(0, icon5)
                    else:
                        # 获取要创建的文件夹路径
                        folder_path = PROJECT_PATH + "//" + itempath+ "//" + folder_name
                        folder_path = file.create_folder(folder_path)
                        folder_name = os.path.basename(folder_path)

                        # 创建item
                        child_item = QTcommand.add_child(self.ui.treeWidget_2, item, name=folder_name)
                        icon5 = QtGui.QIcon()
                        icon5.addPixmap(QtGui.QPixmap(pypath + "\img/folder-dynamic-color.png"), QtGui.QIcon.Normal,
                                        QtGui.QIcon.Off)
                        child_item.setIcon(0, icon5)

            elif action == renameAction:
                self.TreeWeiget_renameItem()

        except Exception as e:
            pass
            # print(e)
    def selectPose(self):
        print("选中物体")
    def Expandmin(self):
        self.ui.dockWidget.setVisible(False)
        self.ui.dockWidget_2.setVisible(False)
        # self.ui.dockWidget_top.setVisible(False)
        self.ui.pushButton_3.setVisible(True)
        self.ui.Btn_Apply2.setVisible(True)
        self.ui.Btn_Menu_2.setVisible(True)
        self.UpdataLibrary()

    def Expandmax(self):
        self.ui.dockWidget.setVisible(True)
        self.ui.dockWidget_2.setVisible(True)
        # self.ui.dockWidget_top.setVisible(True)
        self.ui.pushButton_3.setVisible(False)
        self.ui.Btn_Apply2.setVisible(False)
        self.ui.Btn_Menu_2.setVisible(False)
        self.UpdataLibrary()

    def AddFolder(self):
        global PROJECT_PATH
        # if not self.ui.treeWidget_2.selectedItems():
        folder_name = "folder"

        # 设置要创建的文件夹路径
        folder_path = PROJECT_PATH+"//"+folder_name
        folder_path = file.create_folder(folder_path)

        folder_name = os.path.basename(folder_path)
        item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget_2)
        item.setText(0,folder_name)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(pypath + "\img/folder-dynamic-color.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        item.setIcon(0, icon5)
        self.ui.treeWidget_2.insertTopLevelItems(0, [item])
        self.ui.treeWidget_2.editItem(item)

        # self.ui.treeWidget_2.clear()
        # QTcommand.updataListItem(PROJECT_PATH,self.ui.treeWidget_2)


        #添加子文件夹
        # else:
        #     item = QTcommand.add_child(self.ui.treeWidget_2)
        #
        #     icon5 = QtGui.QIcon()
        #     icon5.addPixmap(QtGui.QPixmap(pypath + "\img/folder-dynamic-color.png"), QtGui.QIcon.Normal,
        #                     QtGui.QIcon.Off)
        #     item.setIcon(0, icon5)
        #     itempath = QTcommand.get_item_path(item)
        #
        #     folderpath = PROJECT_PATH+"\\"+itempath
        #     print(folderpath)
            #创建文件
            # print("xu")

    def creatProject(self):
        global pypath
        global PROJECT_NAME
        global PROJECT_PATH

        my_documents_path = os.path.expanduser('~/Documents')
        configfile = file.check_and_create_file(my_documents_path, 'poselibrary', 'poselibrary.txt')

        folder_path = self.open_file_dialog()
        PROJECT_PATH = folder_path
        PROJECT_NAME = os.path.basename(folder_path)
        project = file.AddProject(PROJECT_PATH)
        file.write_data_to_file(configfile, project)
        self.stepWindowUi()
        QTcommand.pypath = pypath
        QTcommand.updataListItem(PROJECT_PATH, self.ui.treeWidget_2)

        self.ui.Btn_Project.setText(PROJECT_NAME)

        self.ui.dockWidget.setVisible(True)
        self.ui.dockWidget_2.setVisible(True)
        self.ui.UI_Library_frame.setVisible(True)
        self.UpdataLibrary()
        # self.ui.dockWidget_top.setVisible(True)

    def Btn_HomePaggeEvent(self):
        global PROJECT_PATH
        #设置item没有选中
        # self.ui.Btn_HomePagge.setStyleSheet("QPushButton {  background-color:rgb(40, 105, 254);")
        self.ui.Btn_PathTip.setText("首页")
        self.ui.treeWidget_2.clearSelection()
        self.UpdataLibrary()
        # filelist = file.getfile(PROJECT_PATH, ".png")
        # if filelist == []:
        #     self.ui.frame_2.setVisible(False)
        #     self.ui.frame_11.setVisible(True)
        #
        #
        # else:
        #     self.ui.frame_11.setVisible(False)
        #     self.ui.frame_2.setVisible(True)
        # #刷新表格
        #     QTcommand.updataLibraryItem(PROJECT_PATH,self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())

    def TableWeiget_reanameItem(self):
        global PROJECT_PATH
        global LISTITEMPATH
        if not self.ui.tableWidget.currentIndex():
            print(test)
            pass
        else:
            try:
                path = self.getCellPath()
            except:
                pass
            filepath = path + ".json"
            pngpath = path + ".png"
            parent_path = os.path.dirname(path)

            selected = self.ui.tableWidget.selectedIndexes()
            # print(selected)

            for item in selected:
                row = item.row()
                column = item.column()
            frame = self.ui.tableWidget.cellWidget(row, column)
            lineEdits = frame.findChildren(QtWidgets.QLineEdit)
            name = lineEdits[0].text()
            lineEdits[0].setEnabled(True)
            lineEdits[0].setReadOnly(False)
            lineEdits[0].setStyleSheet("QLineEdit{\n"
                                            "    background-color: rgb(255, 255, 255);\n"
                                            "color: rgb(50, 50, 50);}")

            # lineEdits[0].setSelection(0, len(lineEdits[0].text()))

            # lineEdits[0].textChanged()

            def onItemChanged(LEdit=lineEdits[0]):
                name = LEdit.text()
                LEdit.deselect()
                LEdit.setReadOnly(True)
                LEdit.setEnabled(False)
                new_pngpath = parent_path + "//" + name + ".png"
                new_filepath = parent_path + "//" + name + ".json"
                new_pngpath = file.cheak_file(new_pngpath)
                new_filepath = file.cheak_file(new_filepath)
                try:
                    os.rename(filepath,new_filepath)
                    os.rename(pngpath, new_pngpath)
                except:
                    pass
                self.UpdataLibrary()
                # print(new_pngpath)
                return (name)

            # self.ui.treeWidget_2.closePersistentEditor(selectItem, 0)
            lineEdits[0].editingFinished.connect(onItemChanged)
            editor.lineEdit.lineEdits[0]()


    def resetPose(self):
        global PROJECT_PATH
        global LISTITEMPATH
        if not self.ui.tableWidget.currentIndex():
            print(test)
            pass
        else:
            path = self.getCellPath()
            filepath =path+".json"
            pngpath = path+".png"
            posedata = pose.savePose()
            with open(filepath, 'w') as f:
                json.dump(posedata, f)

            render.render_png(300, 300, pngpath)
            self.ui.tableWidget.clear()
            newpath = self.getCellPath()
            QTcommand.updataLibraryItem(newpath, self.ui.tableWidget,
                                        self.ui.centralwidget.frameGeometry().width())

    def CreatPose(self):
        global PROJECT_PATH
        global LISTITEMPATH
        # pose.make_cylinder()
        # name = self.UI_addpose_inputDialog()
        name = "pose"
        jsonname = name + ".json"
        # print(pypath+"\img//picture-dynamic-clay.png")
        if not self.ui.treeWidget_2.selectedItems():


            filepath = PROJECT_PATH +"\\"+jsonname
            pngpath = PROJECT_PATH +"\\"+name+".png"
            new_filepath = file.create_file(filepath)
            new_pngpath = file.create_file(pngpath)


            # open(new_filepath, 'w').close()
            posedata = pose.savePose()

            with open(new_filepath, 'w') as f:
                json.dump(posedata, f)

            render.render_png(300, 300, new_pngpath)
            filelist = file.getfile(PROJECT_PATH, ".png")
            if filelist == []:
                self.ui.frame_2.setVisible(False)
                self.ui.horizontalSlider.setVisible(False)
                self.ui.frame_11.setVisible(True)

            else:
                self.ui.frame_11.setVisible(False)
                self.ui.frame_2.setVisible(True)
                self.ui.horizontalSlider.setVisible(True)

            QTcommand.updataLibraryItem(PROJECT_PATH, self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())
        else :
            #获取路径
            for item in self.ui.treeWidget_2.selectedItems():
                index = self.ui.treeWidget_2.indexOfTopLevelItem(item)
                itempath = QTcommand.get_item_name(item)

                folder_path = PROJECT_PATH + "//" + itempath
                filepath = folder_path + "\\" + jsonname
                pngpath = folder_path + "\\" + name + ".png"
                new_filepath = file.create_file(filepath)
                new_pngpath = file.create_file(pngpath)

                try:
                    open(new_filepath, 'w').close()
                    posedata = pose.savePose()
                    with open(new_filepath, 'w') as f:
                        json.dump(posedata, f)

                    render.render_png(300, 300, new_pngpath)

                    filelist = file.getfile(folder_path, ".png")
                    if filelist == []:
                        self.ui.frame_2.setVisible(False)
                        self.ui.horizontalSlider.setVisible(False)
                        self.ui.frame_11.setVisible(True)

                    else:
                        self.ui.frame_11.setVisible(False)
                        self.ui.frame_2.setVisible(True)
                        self.ui.horizontalSlider.setVisible(True)

                    QTcommand.updataLibraryItem(folder_path, self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())
                except:
                    pass



        return posedata

    def CreatAnim(self):
        global PROJECT_PATH
        global LISTITEMPATH
        def creatanim(filepath,pngpath):

            animedata = anim.saveAnim()
            with open(filepath, 'w') as f:
                json.dump(animedata, f)
            render.render_png(300, 300, pngpath)
            return animedata

        def uiVisble():
            filelist = file.getfile(PROJECT_PATH, ".png")
            if filelist == []:
                self.ui.frame_2.setVisible(False)
                self.ui.horizontalSlider.setVisible(False)
                self.ui.frame_11.setVisible(True)

            else:
                self.ui.frame_11.setVisible(False)
                self.ui.frame_2.setVisible(True)
                self.ui.horizontalSlider.setVisible(True)


        name = "Anim"
        jsonname = name + ".json"

        if not self.ui.treeWidget_2.selectedItems():

            filepath = PROJECT_PATH + "\\" + jsonname
            pngpath = PROJECT_PATH + "\\" + name + ".png"
            new_filepath = file.create_file(filepath)
            new_pngpath = file.create_file(pngpath)
            animdata = creatanim(new_filepath,new_pngpath)
            uiVisble()
            QTcommand.updataLibraryItem(PROJECT_PATH, self.ui.tableWidget,
                                        self.ui.centralwidget.frameGeometry().width())

        else:
            for item in self.ui.treeWidget_2.selectedItems():
                index = self.ui.treeWidget_2.indexOfTopLevelItem(item)
                itempath = QTcommand.get_item_name(item)

                folder_path = PROJECT_PATH + "//" + itempath
                filepath = folder_path + "\\" + jsonname
                pngpath = folder_path + "\\" + name + ".png"
                new_filepath = file.create_file(filepath)
                new_pngpath = file.create_file(pngpath)
                animdata = creatanim(new_filepath, new_pngpath)
                QTcommand.updataLibraryItem(folder_path, self.ui.tableWidget,
                                            self.ui.centralwidget.frameGeometry().width())
        return animdata



    def ApplyPose(self):
        global progressBarValue
        global JSONPATH
        # 定位json路径
        path = JSONPATH
        # 读取数据
        with open(path, 'r') as f:
            posedata = json.load(f)
        #获取设置
        selectobj = cmds.ls()
        # selectobj = cmds.selectobj(posedata)
        count = 2

        self.ui.progressBar.setVisible(True)
        # #多线程
        # t = threading.Thread(target=pose.pastPose,args=(posedata,selectobj,count,self.ui.progressBar))
        # t.start()
        # t.join()
        if self.ui.checkBox_3.isChecked():

            pose.pastPose(posedata, selectobj, count, self.ui.progressBar)
        else:
            pose.pastPoseRot(posedata, selectobj, count, self.ui.progressBar)

        render.reViews()
        self.ui.progressBar.setVisible(False)
        # print(t)
        #cmds.set_transform_keyframes(selectobj)
        #应用pose


    def UI_addpose_inputDialog(self):
        name,ok = QtWidgets.QInputDialog.getText(self,"name","name",QtWidgets.QLineEdit.Normal,"pose")
        if ok :
            return name
    def Click_Treeweiget(self):
        path = self.getCellPath()
        textA = os.path.basename(path)
        self.ui.Btn_PathTip.setText(textA)
        self.removeCradData()
        self.UpdataLibrary()


    def UpdataLibrary(self):
        global LISTITEMPATH
        global PROJECT_PATH



        if not self.ui.treeWidget_2.selectedItems():
            filelist = file.getfile(PROJECT_PATH, ".png")
            if filelist ==[]:
                self.ui.frame_2.setVisible(False)
                self.ui.horizontalSlider.setVisible(False)
                self.ui.frame_11.setVisible(True)

            else:
                self.ui.frame_11.setVisible(False)
                self.ui.frame_2.setVisible(True)
                self.ui.horizontalSlider.setVisible(True)
                QTcommand.updataLibraryItem(PROJECT_PATH, self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())
        else:
            LISTITEMPATH = QTcommand.get_item_path(self.ui.treeWidget_2)
            filelist = file.getfile(PROJECT_PATH + "//" + LISTITEMPATH, ".png")
            if filelist == []:
                self.ui.frame_2.setVisible(False)
                self.ui.horizontalSlider.setVisible(False)
                self.ui.frame_11.setVisible(True)

            else:
                self.ui.frame_11.setVisible(False)
                self.ui.frame_2.setVisible(True)
                self.ui.horizontalSlider.setVisible(True)
                QTcommand.updataLibraryItem(PROJECT_PATH + "//" + LISTITEMPATH, self.ui.tableWidget, self.ui.centralwidget.frameGeometry().width())

        return LISTITEMPATH


    def removeCradData(self):
        global pypath
        self.ui.Lbl_Name.setText("name: " )
        self.ui.Lbl_ObjCount.setText("None Objects")
        QTcommand.BtnSetIcons(self.ui.pushButton_4, pypath + "\img//picture-dynamic-clay.png")
        self.ui.pushButton_4.setIconSize(QtCore.QSize(200, 200))
        self.ui.Lbl_Path.setText(("None Path"))
    def UpdataCradData(self):
        """
        刷新预览图和文件信息
        :return:
        """
        #获取选中的ite
        global PROJECT_PATH
        global LISTITEMPATH
        global JSONPATH
        global CellRelativePath

        path = self.getCellPath()

        SELECTITEMPATH = path+".png"
        JSONPATH = path+".json"
        JSONPATH = u"{}".format(JSONPATH)
        name = file.getfileName(SELECTITEMPATH)
        try:
            with open(JSONPATH, 'r') as f:
                posedata = json.load(f)
            #判断类型：
            if posedata[0]["starttime"]:
                print("flase")
                count = pose.getselectobjcount(posedata)
                QTcommand.BtnSetIcons(self.ui.pushButton_4, SELECTITEMPATH)
                self.ui.pushButton_4.setIconSize(QtCore.QSize(200, 200))
                self.ui.Lbl_Name.setText("name: " + name)
                self.ui.Lbl_ObjCount.setText("{} Objects".format(count))
                self.ui.Lbl_Path.setText(CellRelativePath)
            else:
                print("flase")
                posedata = posedata[1]
                count = pose.getselectobjcount(posedata)
                QTcommand.BtnSetIcons(self.ui.pushButton_4, SELECTITEMPATH)
                self.ui.pushButton_4.setIconSize(QtCore.QSize(200, 200))
                self.ui.Lbl_Name.setText("name: " + name)
                self.ui.Lbl_ObjCount.setText("{} Objects".format(count))
                self.ui.Lbl_Path.setText(CellRelativePath)
        except:
            pass



        return JSONPATH

    def workflow(self):
        global  pypath
        global PROJECT_PATH
        global PROJECT_NAME
        try:
            my_documents_path = os.path.expanduser('~/Documents')
            file_path = file.check_and_create_file(my_documents_path, 'poselibrary', 'poselibrary.txt')
            projectdata = file.read_file(file_path)
            projectdata = json.loads(projectdata)
            PROJECT_PATH = projectdata["ProjectPath"]
            PROJECT_NAME = projectdata["ProjectName"]
            self.size_changed.disconnect(self.eventItemSort)
        except:
            pass
        # print(type(projectdata))

        # print(PROJECT_PATH, PROJECT_NAME)


        if PROJECT_PATH =="":
            self.ui.pushButton_5.setFocusPolicy(QtCore.Qt.NoFocus)

            # self.ui.lineEdit_2.setFocusPolicy(QtCore.Qt.NoFocus)
            self.startWindwoUi()
            self.show()
            self.center()

        else:

            self.stepWindowUi()


            self.ui.frame_9.setVisible(False)
            self.Btn_HomePaggeEvent()
            QTcommand.pypath = pypath
            QTcommand.updataListItem(PROJECT_PATH, self.ui.treeWidget_2)
            self.show()
            self.Btn_HomePaggeEvent()
            self.center()
            self.Btn_HomePaggeEvent()
            self.size_changed.connect(self.eventItemSort)
            self.Btn_HomePaggeEvent()





            # QTcommand.pypath = pypath
            # QTcommand.updataListItem(PROJECT_PATH, self.ui.treeWidget_2)
            # self.ui.treeWidget_2.clearSelection()
            # QTcommand.updataLibraryItem(PROJECT_PATH, self.ui.tableWidget,self.ui.centralwidget.frameGeometry().width())


    def startWindwoUi(self):
        self.ui.dockWidget.setVisible(False)
        self.ui.dockWidget_2.setVisible(False)
        self.ui.UI_Library_frame.setVisible(False)
        self.ui.dockWidget_top.setVisible(False)
        self.ui.Btn_Apply2.setVisible(False)
        self.ui.frame_9.setVisible(True)




    def getCellPath(self):
        global PROJECT_PATH
        global CellPath
        global CellRelativePath
        if not self.ui.treeWidget_2.selectedItems():
            if not self.ui.tableWidget.selectedIndexes():

                CellPath = PROJECT_PATH
                CellRelativePath = ""
            else:
                selected = self.ui.tableWidget.selectedIndexes()
                # print(selected)

                for item in selected:
                    row = item.row()
                    column = item.column()
                try:
                    frame = self.ui.tableWidget.cellWidget(row, column)
                    lineEdits = frame.findChildren(QtWidgets.QLineEdit)
                    name = lineEdits[0].text()
                    CellPath = PROJECT_PATH + "//" + name
                    CellRelativePath = name
                except:
                    pass

        else:
            itempath = QTcommand.get_item_path(self.ui.treeWidget_2)
            if not self.ui.tableWidget.selectedIndexes():
                CellPath = PROJECT_PATH+"//"+itempath
                CellRelativePath = itempath
            else:
                selected = self.ui.tableWidget.selectedIndexes()
                # print(selected)

                for item in selected:
                    row = item.row()
                    column = item.column()
                try:
                    frame = self.ui.tableWidget.cellWidget(row, column)
                    lineEdits = frame.findChildren(QtWidgets.QLineEdit)
                    name = lineEdits[0].text()
                    CellPath = PROJECT_PATH + "//"+itempath+"//" + name
                    CellRelativePath = itempath+"//" + name
                except:
                    pass
        CellPath = u"{}".format(CellPath)
        CellRelativePath =  u"{}".format(CellRelativePath)
        return CellPath
    def stepWindowUi(self):
        # window.ui.statusbar.setVisible(False)
        #self.ui.statusbar.setFixedSize(600,5)
        self.ui.statusbar.setStyleSheet("QStatusBar {background: transparent;}"
                                "QStatusBar::item {"
                                "border: 1px solid red;"
                                "border-radius: 3px;"
                                "}")

        # self.ui.treeWidget_2.setStyleSheet("QTreeView::branch {background: transparent;}")
        # self.ui.treeWidget_2.setStyleSheet("QTreeView::branch:!adjoins-item {border-image: url(vline.png) 0;}")
        # self.ui.treeWidget_2.setStyleSheet("QTreeView::branch:adjoins-item {border-image: url(branch-more.png) 0;}")
        self.docktitle = QtWidgets.QWidget()
        self.docktitle_2 = QtWidgets.QWidget()
        self.docktitle_top = QtWidgets.QWidget()
        self.docktitle_down = QtWidgets.QWidget()
        self.ui.dockWidget.setTitleBarWidget(self.docktitle)
        self.ui.dockWidget_2.setTitleBarWidget(self.docktitle_2)
        self.ui.dockWidget_top.setTitleBarWidget(self.docktitle_top)
        self.ui.dockWidget_down.setTitleBarWidget(self.docktitle_down)
        self.ui.pushButton_3.setVisible(False)
        self.ui.pushButton.setVisible(False)
        self.ui.dockWidget_top.setVisible(False)
        self.ui.Btn_Apply2.setVisible(False)
        self.ui.Btn_Apply2.setVisible(False)
        self.ui.frame_9.setVisible(False)
        self.ui.Btn_Menu_2.setVisible(False)
        QTcommand.BtnSetIcons(self.ui.Btn_Menu, pypath + "\img//cube-iso-clay.png", size = 30)
        QTcommand.BtnSetIcons(self.ui.Btn_Menu_2, pypath + "\img//cube-iso-clay.png", size = 30)
        QTcommand.BtnSetIcons(self.ui.Btn_Add, pypath + "\img//new-folder-dynamic-color.png", size = 30)
        QTcommand.BtnSetIcons(self.ui.Btn_Expand, pypath + "\img//figma-dynamic-clay.png", size = 30)
        QTcommand.BtnSetIcons(self.ui.Btn_Creat, pypath + "\img//plus-dynamic-clay.png", size = 30)
        QTcommand.BtnSetIcons(self.ui.Btn_Creat_Anim, pypath + "\img//plus-dynamic-clay.png", size=30)
        QTcommand.BtnSetIcons(self.ui.pushButton_4, pypath + "\img//picture-dynamic-clay.png", size = 30)
        QTcommand.BtnSetIcons(self.ui.pushButton_3, pypath + "\img//figma-dynamic-clay.png", size = 30)
        QTcommand.BtnSetIcons(self.ui.Btn_HomePagge, pypath + "\img/folder-dynamic-color.png", Text ="首页", size = 23)

        self.ui.pushButton_4.setIconSize(QtCore.QSize(200, 200))
        Pixmap = QtGui.QPixmap(pypath + "\img//puzzle-dynamic-clay.png")
        # Pixmap.scaled(40, 40)
        self.ui.label_5.setPixmap(Pixmap)


        self.ui.dockWidget.widget().setMinimumSize(QtCore.QSize(200, 150))
        self.ui.dockWidget.widget().setMaximumSize(QtCore.QSize(200, 150000))
        # window.ui.dockWidget_2.widget().setMinimumSize(QtCore.QSize(150, 400))
        self.ui.dockWidget_2.widget().setMaximumSize(QtCore.QSize(400, 150000))

        self.ui.Btn_Project.setText (PROJECT_NAME)

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
        self.ui.Btn_Apply2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.horizontalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Temp_CopyPose.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Temp_PastPose.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Temp_CopyXform.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Temp_PastXform.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Temp_ResetPose.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.pushButton_7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.pushButton_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.checkBox_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.checkBox_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Apply.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.horizontalSlider_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Menu_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_PathTip.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Project.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.Btn_Creat_Anim.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.CBox_Sort.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.CBox_Type.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui.Btn_Add.setToolTip("添加文件夹")
        self.ui.pushButton.setToolTip("添加文件夹")
        self.ui.Btn_Expand.setToolTip("隐藏-左栏\右栏")
        self.ui.pushButton_3.setToolTip("显示-左栏\右栏")
        self.ui.Btn_Creat.setToolTip("添加Pose")
        self.ui.Btn_Apply.setToolTip("应用Pose")
        self.ui.Btn_Apply2.setToolTip("应用Pose")
        self.ui.checkBox_3.setToolTip("")
        self.ui.checkBox_4.setToolTip("")


        # print("设置UI样式")

        self.ui.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  #设置只能单选

    def center(self):
        self.setGeometry(12,120,900,600)
        qr = self.frameGeometry()
        # print(qr)
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        self.move(qr.topLeft())
    def handle_timeout(self):
        self._blocked = False

    def resizeEvent(self, event):
        if not self._timer.isActive():
            self.size_changed.emit(event.size().width(), event.size().height())
            self._blocked = True
            self._timer.start(10) # 屏蔽信号的时间，单位毫秒
        elif not self._blocked:
            self._timer.stop()
            self._timer.start(10)
            self._blocked = True
        super(MainWindow, self).resizeEvent(event)

    # def mousePressEvent(self, event):
    #     if event.button() ==QtCore.Qt.LeftButton and self.isMaximized() ==False:
    #         self.m_flag = True
    #         self.m_Position = event.globalPos() -self.pos()
    #         event.accept()
    #         self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
    # def mouseMoveEvent(self, mouse_event):
    #     if QtCore.Qt.LeftButton and self.m_flag:
    #         self.move(mouse_event.globalPos() - self.m_Position)
    #         mouse_event.accept()
    # def mouseReleaseEvent(self, mouse_event):
    #     self.m_flag = False
    #     self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()

        else:
            self.showMaximized()

    # def wheelEvent(self, event):
    #     if event.modifiers() == QtCore.Qt.ControlModifier:
    #         self.ui.horizontalSlider.wheelEvent(event)

    def itemsort(self):
        # time.sleep(0.25)
        self.UpdataLibrary()


    def eventItemSort(self,w, h):
        QTimer.singleShot(50, self.itemsort)
        # print("yes yes yes")

        gc.collect()  # python内置清除内存函数
    def eventFilter(self, watched, event):
        if watched == self.ui.tableWidget and event.type() == QtCore.QEvent.Wheel:
            if event.modifiers() == QtCore.Qt.ControlModifier:
                # 在这里执行你想要绑定的操作
                self.ui.horizontalSlider.wheelEvent(event)
                return True
        # if watched == self.ui.tableWidget and event.type() == QtCore.QEvent.KeyPress:
        #     if event.key() == QtCore.Qt.Key_F2:
                # print("重命名")

        return super(MainWindow, self).eventFilter(watched, event)
    # def evenrfilter(self,eventlist):
    #     for event in eventlist:
    #         self.ui.Btn_Creat.installEventFilter(event)
def main():
    global  PROJECT_PATH
    global  LISTITEMPATH
    from PySide2 import shiboken2
    from pymxs import runtime as rt
    global pypath
    # rt.resetMaxFile(rt.name('noPrompt'))
    # Cast the main window HWND to a QMainWindow for docking
    # First, get the QWidget corresponding to the Max windows HWND:
    main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())
    # Then cast it as a QMainWindow for docking purposes:
    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)



    window = MainWindow(main_window)
    # window = MainWindow()
    path = PROJECT_PATH+"//"+LISTITEMPATH
    window.show()


def test():
    pypath = os.getcwd()
    # print (pypath)
    if pypath in sys.path:
        pass
    else:
        sys.path.append(pypath)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    return window

if __name__ == "__main__":
    pass
    #pycharme run code//////////////