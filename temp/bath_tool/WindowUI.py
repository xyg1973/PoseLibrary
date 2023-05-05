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
        print(module_name)
        print("重新加载失败")
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


def BtnSetIcons(PushButton,iconsPath,Text = ""):
	icon_img = QtGui.QIcon()
	icon_img.addPixmap(QtGui.QPixmap(iconsPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	PushButton.setIcon(icon_img)
	# PushButton.setIconSize(QtCore.QSize(size, size))
	PushButton.setText(Text)

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


def mxs_get_all_children(parent, node_type=None):
    """Handy function to get all the children of a given node

    Args:
        parent (3dsmax Node1): node to get all children of
        node_type (None, runtime.class): give class to check for
                                         e.g. rt.FFDBox/rt.GeometryClass etc.

    Returns:
        list: list of all children of the parent node
    """
    def list_children(node):
        children = []
        for c in node.Children:
            children.append(c)
            children = children + list_children(c)
        return children
    child_list = list_children(parent)

    return ([x for x in child_list if rt.superClassOf(x) == node_type]
            if node_type else child_list)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = bath_tool.Ui_mainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("SN_Anim_Batch_Tool")
        self.stepWindowUi()
        self.creat_contion()
        self.test_model()

    def test_model(self):
        self.ui.LEditA_svae_path.setText("")
        self.ui.LEditA_max_path.setText("H:\\work\\SNGame\\2023\\202304\\loco\\MAX\\算飘带的动画\\成男持械_算飘带文件")
        self.ui.LEditA_newSkin.setText("H:\\work\\SNGame\\ArtHub\\Skin_文件\\主角\\吴六鼎\\M_3009_skin.max")
        self.UpdataListA()
    def creat_contion(self):
        # self.ui.menu_2.clicked.connect(self.showlogUI)
        # self.ui.menu_2.actions(self.showlogUI)
        self.ui.Menu_Right.itemClicked.connect(self.clicked_Menu_Right)
        self.ui.Btn_setting.clicked.connect(self.clicked_Btn_setting)

        self.ui.Btn_message_tip_close.clicked.connect(self.closeMessage)
        self.ui.Btn_message_error_close.clicked.connect(self.closeMessage)
        self.ui.Btn_message_success_close.clicked.connect(self.closeMessage)


        #动画-批量替换模型页按钮事件
        self.ui.BtnA_newSkin.clicked.connect(self.clicked_BtnA_newSkin)
        self.ui.BtnA_max_path.clicked.connect(self.clicked_BtnA_max_path)
        self.ui.BtnA_max_path_open.clicked.connect(self.clicked_BtnA_max_path_open)
        self.ui.BtnA_svae_path.clicked.connect(self.clicked_BtnA_svae_path)
        self.ui.BtnA_svae_path_auto.clicked.connect(self.clicked_BtnA_svae_path_auto)
        self.ui.BtnA_svae_path_open.clicked.connect(self.clicked_BtnA_svae_path_open)
        self.ui.BtnA_max_path_Pick.clicked.connect(self.clicked_BtnA_max_path_Pick)
        self.ui.LEditA_max_path.textEdited.connect(self.UpdataListA)
        self.ui.BtnA_RefreshList.clicked.connect(self.UpdataListA)
        self.ui.BtnA_List_select_all.clicked.connect(self.clicked_BtnA_List_select_all)
        self.ui.BtnA_List_select_reverse.clicked.connect(self.clicked_BtnA_List_select_reverse)
        self.ui.BtnA_Apply.clicked.connect(self.Apply)


        #动画-批量导出FBX页按钮事件
        self.ui.BtnB_svae_path.clicked.connect(self.clicked_BtnB_svae_path)
        self.ui.BtnB_svae_path_open.clicked.connect(self.clicked_BtnB_svae_path_open)
        self.ui.BtnB_svae_path_auto.clicked.connect(self.clicked_BtnB_svae_path_auto)
        self.ui.BtnB_max_path.clicked.connect(self.clicked_BtnB_max_path)
        self.ui.BtnB_max_path_open.clicked.connect(self.clicked_BtnB_max_path_open)
        self.ui.BtnB_RefreshList.clicked.connect(self.UpdataListB)
        self.ui.LEditB_max_path.textEdited.connect(self.UpdataListB)
        self.ui.LEditB_max_path.textEdited.connect(self.UpdataListB)
        self.ui.BtnB_RefreshList.clicked.connect(self.UpdataListB)
        pass

    def stepWindowUi(self):
        # 隐藏标题栏
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        item = self.ui.Menu_Right.topLevelItem(0)
        self.ui.Menu_Right.setCurrentItem(item)
        self.clicked_Menu_Right()

        #设置icon
        iconpath_folder = "C:\Program Files\Autodesk\\3ds Max 2020\python\PoseLibrary\\temp\\bath_tool\ui\\folder-dynamic-color.png"
        BtnSetIcons(self.ui.BtnA_svae_path,iconpath_folder)
        BtnSetIcons(self.ui.BtnA_max_path, iconpath_folder)
        BtnSetIcons(self.ui.BtnA_newSkin, iconpath_folder)
        BtnSetIcons(self.ui.BtnB_svae_path, iconpath_folder)
        BtnSetIcons(self.ui.BtnB_max_path, iconpath_folder)



        self.docktitle = QtWidgets.QWidget()
        self.docktitle_2 = QtWidgets.QWidget()
        self.docktitle_3 = QtWidgets.QWidget()
        self.ui.dockWidget.setTitleBarWidget(self.docktitle)
        self.ui.dockWidget_2.setTitleBarWidget(self.docktitle_2)
        self.ui.dockWidget_3.setTitleBarWidget(self.docktitle_3)

        # self.ui.dockWidget_2.setMinimumSize(QtCore.QSize(480, 660))
        self.ui.dockWidget_2.setVisible(False)
        self.ui.dockWidget_3.setVisible(False)
        self.ui.progressBar.setVisible(False)

        self.setStyleSheet("QMainWindow#MainWindow\n"
                           "{\n"
                           "background-color:rgb(200, 200, 200);\n"
                           "}    \n"
                           "")

        self.ui.treeWidgetA.clear()
        self.ui.treeWidgetB.clear()

        self.ui.treeWidgetA.setColumnWidth(0,30)
        self.ui.treeWidgetA.setColumnWidth(1, 200)
        self.ui.treeWidgetA.setColumnWidth(2, 600)

        self.ui.treeWidgetB.setColumnWidth(0,30)
        self.ui.treeWidgetB.setColumnWidth(1, 200)
        self.ui.treeWidgetB.setColumnWidth(2, 600)

        self.ui.groupBox_14.setVisible(False)

        self.ui.frame_message.setVisible(False)


    def actionshow_log(self):
        self.ui.dockWidget_2.setVisible(True)
        self.ui.dockWidget_3.setVisible(True)


    def actionhide_log(self):
        self.ui.dockWidget_2.setVisible(False)
        self.ui.dockWidget_3.setVisible(False)

    # def showlogUI(self):
    #     self.ui.dockWidget_2.setVisible(True)
    #     self.ui.dockWidget_3.setVisible(True)
    def closeMessage(self):
        self.ui.frame_message.setVisible(False)

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
        self.ui.LEditA_newSkin.setText(folder_path)

    def clicked_BtnA_max_path(self):
        folder_path = self.dialog_getMaxFileDir()
        if folder_path!="":
            print(folder_path)
            self.ui.LEditA_max_path.setText(folder_path)
            self.UpdataListA()
        else:
            print("文件为空")

    def clicked_BtnA_max_path_open(self):
        maxpath = self.ui.LEditA_max_path.text()
        try:
            os.startfile(maxpath)
        except:
            pass

    def clicked_BtnA_svae_path(self):
        folder_path = self.dialog_getMaxFileSaveDir()
        print(folder_path)
        self.ui.LEditA_svae_path.setText(folder_path)

    def clicked_BtnA_svae_path_auto(self):
        max_folder_path = self.ui.LEditA_max_path.text()
        folder_path = max_folder_path+"/NewFile"
        self.ui.LEditA_svae_path.setText(folder_path)
    def clicked_BtnA_svae_path_open(self):
        #判断文件夹是否存在
        svae_path = self.ui.LEditA_svae_path.text()
        try:
            os.startfile(svae_path)
        except:
            pass

    def clicked_BtnA_max_path_Pick(self):
        skinpath = rt.maxFilePath+rt.maxFileName
        self.ui.LEditA_newSkin.setText(skinpath)


    def clicked_BtnA_List_select_all(self):

        self.ui.treeWidgetA.selectAll()


    def clicked_BtnA_List_select_reverse(self):
        selectitem = self.ui.treeWidgetA.selectedItems()
        tree_widget = self.ui.treeWidgetA
        for i in range(tree_widget.topLevelItemCount()):
            item = tree_widget.topLevelItem(i)
            if self.ui.treeWidgetA.isItemSelected(item):
                item.setSelected(False)
            else:
                item.setSelected(True)


    def clicked_BtnB_max_path(self):
        folder_path = self.dialog_getMaxFileDir()
        if folder_path != "":
            print(folder_path)
            self.ui.LEditB_max_path.setText((folder_path))
            self.UpdataListB()
        else:
            print("文件为空")
    def clicked_BtnB_max_path_open(self):

        maxpath = self.ui.LEditB_max_path.text()
        try:
            os.startfile(maxpath)
        except:
            pass


    def clicked_BtnB_svae_path(self):
        folder_path = self.dialog_getMaxFileSaveDir()
        self.ui.LEditB_svae_path.setText(folder_path)

    def clicked_BtnB_svae_path_open(self):
        svaepath = self.ui.LEditB_svae_path.text()
        try:
            os.startfile(svaepath)
        except:
            pass

    def clicked_BtnB_svae_path_auto(self):
        max_folder_path = self.ui.LEditB_max_path.text()
        folder_path = max_folder_path + "/FBX"
        self.ui.LEditB_svae_path.setText(folder_path)


    def clicked_Menu_Right(self):
        item = self.ui.Menu_Right.selectedItems()
        itemtext = item[0].text(0)
        row = self.ui.Menu_Right.indexOfTopLevelItem(item[0])
        if row ==0:
            self.ui.frame_anim.setVisible(True)
            self.ui.frame_rig.setVisible(False)
        elif row ==1:
            self.ui.frame_anim.setVisible(False)
            self.ui.frame_rig.setVisible(True)
        else:
            pass

    def clicked_Btn_setting(self):
        rightMenu = QtWidgets.QMenu(self.ui.Btn_setting)

        fileAction = rightMenu.addAction(u"文件")
        settingAction = rightMenu.addAction(u"设置")
        hidelogAction = rightMenu.addAction(u"显示处理日志")
        aboutAction = rightMenu.addAction(u"关于")
        action = rightMenu.exec_(QtGui.QCursor.pos())
        if action == fileAction:
            print("文件")
            pass
        elif action == hidelogAction:
            self.actionshow_log()

    def UpdataListA(self):
        try:

            self.ui.treeWidgetA.clear()
            folder_path = self.ui.LEditA_max_path.text()
            self.UpdataList_do(self.ui.treeWidgetA,folder_path)
        except:
            pass
    def UpdataListB(self):
        try:
            self.ui.treeWidgetB.clear()
            folder_path = self.ui.LEditB_max_path.text()
            self.UpdataList_do(self.ui.treeWidgetB,folder_path)
        except:
            pass

    def UpdataList_do(self,treeWidget,folder_path):
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

    def Apply(self):
        #判断活动页面
        currentIndex = self.ui.tabWidget_Anim.currentIndex()
        if currentIndex==0:
            self.ApplyB()
        elif currentIndex==1:
            self.ApplyA()





    def Apply_message(self,num=0,text="请检查"):
        """
        num =0;成功
        num= 1; 错误窗口
        num = 2 ; 提示窗口

        """
        num = num
        messagetext = text
        self.ui.frame_message.setVisible(True)
        if num ==0 :
            self.ui.frame_message_tip.setVisible(False)
            self.ui.frame_message_error.setVisible(False)
            self.ui.frame_message_success.setVisible(True)
        elif num == 1:
            self.ui.frame_message_tip.setVisible(False)
            self.ui.frame_message_error.setVisible(True)
            self.ui.frame_message_success.setVisible(False)
        elif num == 2:
            self.ui.frame_message_tip.setVisible(True)
            self.ui.label_message_tip.setText(messagetext)
            self.ui.frame_message_error.setVisible(False)
            self.ui.frame_message_success.setVisible(False)



    def ApplyB_check(self):
        savepath = self.ui.LEditB_svae_path.text()
        maxfilepath = self.ui.LEditB_max_path.text()

        selectitems = self.ui.treeWidgetB.selectedItems()
        if len(selectitems)>0:
            try:
                os.mkdir(savepath)
            except:
                pass
            if os.path.exists(savepath):
                self.ui.BtnA_Apply.setEnabled(False)
                return True
            else:
                self.Apply_message(num=2, text="请检查保存路径是否存在")
        else:
            self.Apply_message(num=2, text="请选中要执行的文件")

    def ApplyB(self):

        savepath = self.ui.LEditB_svae_path.text()
        maxfilepath = self.ui.LEditB_max_path.text()

        # 判断skin文件是否存在
        checkfile = self.ApplyB_check()
        if checkfile == True:
            self.ui.BtnA_Apply.setEnabled(True)
            self.ui.frame_message.setVisible(False)
            self.ui.progressBar.setVisible(True)
            selectitems = self.ui.treeWidgetB.selectedItems()

            max = len(selectitems)
            k = 0
            self.ui.progressBar.setValue(float(k) / float(max) * 100)
            for item in selectitems:
                self.ui.progressBar.setValue(float(k) / float(max) * 100)
                print ("开始执行导出FBX")

                path = item.text(2)
                print(path)
                rt.loadMaxFile(path, quiet=True)

                k += 1
                self.ui.progressBar.setValue(float(k) / float(max) * 100)

            self.ui.progressBar.setVisible(False)
            self.ui.BtnA_Apply.setEnabled(True)
            self.ui.frame_message.setVisible(True)
            self.Apply_message(num=0)


    def ApplyA_check(self):
        newskinpath = self.ui.LEditA_newSkin.text()
        savepath = self.ui.LEditA_svae_path.text()
        maxfilepath = self.ui.LEditA_max_path.text()

        if os.path.exists(newskinpath):     #判断skin文件是否存在
            selectitems = self.ui.treeWidgetA.selectedItems()
            if len(selectitems) > 0:
                if os.path.exists(savepath):  # 判断保存路径是否存在
                    self.ui.frame_message.setVisible(False)
                    return True
                else:
                    try:
                        os.mkdir(savepath)
                        self.ui.frame_message.setVisible(False)
                        return True
                    except:
                        self.Apply_message(num=2, text="请检查保存路径是否存在")
                        # print("检查保存路径是否存在")
            else:
                self.Apply_message(num=2, text="请选中要执行的文件")

        else:
            self.Apply_message(num=2,text="请检查skin文件是否存在")


    def ApplyA(self):
        newskinpath = self.ui.LEditA_newSkin.text()
        savepath = self.ui.LEditA_svae_path.text()
        maxfilepath = self.ui.LEditA_max_path.text()

        #判断skin文件是否存在
        checkfile = self.ApplyA_check()
        if checkfile==True :
            #应用按钮屏蔽
            self.ui.BtnA_Apply.setEnabled(False)
            datapath = savepath + "/anim_data"
            try:
                os.mkdir(datapath)
            except:
                pass
                print("文件夹已经存在")
            selectitems =self.ui.treeWidgetA.selectedItems()
            self.ui.progressBar.setVisible(True)
            max = len(selectitems)
            k=0
            self.ui.progressBar.setValue(float(k) / float(max) * 100)
            for item in selectitems:
                self.ui.progressBar.setValue(float(k) / float(max) * 100)
                path = item.text(2)
                # print(item.text(2))
            # try:
                rt.loadMaxFile(path,quiet=True)
                rt.frameRate = 60   #设置帧速率
                timeRange_start = rt.animationRange.start.frame
                timeRange_end = rt.animationRange.end.frame
                rt.redrawViews()
                if self.ui.CBoxA_bip_only.isChecked()==False:
                    #保存xaf文件
                    rootobj = rt.getNodeByName('root')
                    allchildren = mxs_get_all_children(rootobj)
                    allchildren.append(rootobj)
                    xafobjs = allchildren
                    xafpath  = datapath +"/"+item.text(1)+".xaf"
                    if self.ui.CBoxA_iskeyframe.isChecked()==True:
                        print("关键帧yes")
                        rt.loadsaveanimation.saveanimation(xafpath,xafobjs,"","",keyableTracks=True)  #keyableTracks关键帧模式
                    else:
                        print("关键帧no")
                        rt.loadsaveanimation.saveanimation(xafpath, xafobjs, "", "", animatedTracks=True,keyableTracks=False,segKeyPerFrame=False)  # keyableTracks关键帧模式


                #保存bip动画
                bippath = datapath + "/" + item.text(1) + ".bip"  # 保存bip动画文件
                objA = rt.getNodeByName('Bip001')
                rt.biped.saveBipFile(objA.controller, bippath)


                #加载新的skin文件
                rt.loadMaxFile(newskinpath,quiet=True)
                rt.frameRate = 60
                rt.redrawViews()
                objA = rt.getNodeByName('Bip001')
                rt.biped.loadBipFile(objA.controller,bippath)
                rt.animationRange = rt.interval(timeRange_start,timeRange_end)      #设置时间滑块范围

                #加载xaf动画
                if self.ui.CBoxA_bip_only.isChecked() == False:
                    rootobj = rt.getNodeByName('root')
                    allchildren = mxs_get_all_children(rootobj)
                    allchildren.append(rootobj)
                    xafobjs = allchildren
                    rt.LoadSaveAnimation.loadAnimation(xafpath,xafobjs)

                savefliepath = savepath+"/"+item.text(1)+".max"
                rt.saveMaxFile(savefliepath)
                print(savefliepath)
                # except:
                #     print("读取文件错误")
                k+=1
                self.ui.progressBar.setValue(float(k) / float(max) * 100)
            self.ui.progressBar.setVisible(False)
            self.ui.BtnA_Apply.setEnabled(True)
            self.Apply_message(num=0)


def main():

    # rt.resetMaxFile(rt.name('noPrompt'))
    # Cast the main window HWND to a QMainWindow for docking
    # First, get the QWidget corresponding to the Max windows HWND:
    main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())
    # Then cast it as a QMainWindow for docking purposes:
    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)
    window = MainWindow(main_window)
    window.show()