import sys
import os
#sys.path.append("H:/pycharm_max_work/poselibray")
#sys.path.remove("H:/pycharm_max_work/poselibray")
def reloadmoudle():
    reload(main)
    reload(Card_Farme)
    reload(List_Farme)
    reload( QTcommand)
    reload(Library_Frame)


reloadmoudle()
#syspath = sys.path
#for i in syspath:
#	print(i)

from PySide2 import QtCore, QtGui, QtWidgets
from UI import main
from UI import Card_Farme
from UI import List_Farme
from UI import Library_Frame
from Tools import file , QTcommand
from PySide2.QtCore import QTimer
import gc
import time



DESINGNPATH ="H:\pycharm_maya_work\Design"

DockWidget = main.main()

# CardA = Card_Farme.Card_Frame(DockWidget.Card_Frame)
# DockWidget.verticalLayout_12.addWidget(CardA)
# CardA.show()


ListA= List_Farme.List_Frame(DockWidget.dockWidget)

DockWidget.verticalLayout_7.addWidget(ListA)
ListA.show()

LibraryA = Library_Frame.Library_Frame(DockWidget.Library_Frame)
DockWidget.verticalLayout_11.addWidget(LibraryA)
LibraryA.show()
LibraryA.tableWidget.clear()
AllItemFrame = QTcommand.updataLibraryItem("H:\pycharm_maya_work\Design//test",LibraryA.tableWidget,LibraryA.width())
#List刷新

QTcommand.itemsort(LibraryA.tableWidget,AllItemFrame)


ListA.treeWidget.clear()
ListA.treeWidget_2.clear()
ListA.treeWidget_2.setVisible(False)
QTcommand.updataListItem(DESINGNPATH,ListA.treeWidget)
force_name = file.getforceName(DESINGNPATH)
#print(force_name)

def itemsort(table = LibraryA.tableWidget,allitem=AllItemFrame):
    #time.sleep(0.25)
    QTcommand.itemsort(table, allitem)


def eventItemSort(w,h):
    QTimer.singleShot(2,itemsort)
    #print("yes yes yes")

    gc.collect()#python内置清除内存函数
#创建事件信号
size_changed_signal = DockWidget.size_changed

#给信号绑定事件
size_changed_signal.connect(eventItemSort)

