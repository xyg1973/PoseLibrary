# -*- coding: utf-8 -*-
import sys
import os
from PySide2 import QtCore, QtGui, QtWidgets
from Tools import file

pypath = ""
itemWidth =200


class MyWidget(QtWidgets.QWidget):
	_TableSignal = QtCore.Signal(int,int)
	def __init__(self, row, column, table_widget, pngpath,parent=None):
		super(MyWidget,self ).__init__(parent)
		self.row = row
		self.column = column
		self.table_widget = table_widget

		# 创建子小部件
		self.layout = QtWidgets.QVBoxLayout(self)
		self.button = QtWidgets.QPushButton()
		self.button .setFocusPolicy(QtCore.Qt.NoFocus)
		self.button.setStyleSheet("QPushButton {\n"
										"    background-color:argb(10, 10, 10,40);\n"
										"    color: rgb(225, 225, 225);\n"
										"    border-width: 0px;\n"
										"    border-radius: 3px;\n"
										"    border-color: beige;\n"
										"    padding: 2px;\n"
										"\n"
										"}\n"
										"QPushButton:hover {\n"
										"    background-color:argb(10, 10, 10,40);\n"
										"}\n"
										"QPushButton:pressed {\n"
										"    background-color: argb(10, 10, 10,40);\n"
										"    border-style: inset;\n"
										"}\n"
										"")
		# pixmap = QtGui.QPixmap(pngpath)
		# pixmap.scaled(40, 40)
		# self.label.setPixmap(pixmap)
		# self.label.resize(QtCore.QSize(40,40))
		self.lineEdit = QtWidgets.QLineEdit()
		self.lineEdit.setStyleSheet("QLineEdit{\n"
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

		# 添加到布局中
		self.layout.addWidget(self.button)
		self.layout.addWidget(self.lineEdit)

		#安装事件过滤器
		self.installEventFilter(self)
		self.button.installEventFilter(self)
		# self.lineEdit.installEventFilter(self)

	# 信号事件选中item中部件会同时选中item
	def eventFilter(self, watched,tableweigetevent ):
		if tableweigetevent.type() == QtCore.QEvent.MouseButtonPress:
			self.table_widget.setCurrentCell(self.row,self.column )
			item = self.table_widget.item(self.row,self.column )
			self.table_widget.setItemSelected(item,True )
			return True
		if tableweigetevent.type() == QtCore.QEvent.MouseButtonDblClick:
			self.table_widget.setCurrentCell(self.row, self.column)
			self._TableSignal.emit(self.row,self.column)
			print("双击事件")
		try:
			return super(MyWidget,self ).eventFilter(watched,tableweigetevent )
		except:
			return None

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	window = QtWidgets.QMainWindow()
	tableWidget = QtWidgets.QTableWidget(4 ,4 ,window )
	window.setCentralWidget(tableWidget)
def treeWidgetStyleSheet(treeWidget):
	treeWidget.setStyleSheet("QTreeWidget\n"
"{\n"
"background-color: transparent;\n"
"color:rgb(255, 255, 255);\n"
"border: 0px solid rgb(17, 17, 17);\n"
"}    \n"
"QTreeWidget::item {\n"
"    background-color:transparent;\n"
"    color: rgb(255, 255, 255);\n"
"    border-width: 0px;\n"
"    border-radius: 3px;\n"
"    border-color: beige;\n"
"    padding: 2px;\n"
"    text-align:left;\n"
"    height:23px;\n"
"}\n"
"QTreeWidget::item:hover {\n"
"    background-color: rgb(52, 95, 251);\n"
"}\n"
"QTreeWidget::item:pressed {\n"
"    background-color: rgb(10, 50, 205);\n"
"    border-style: inset;\n"
"}\n"
"\n"
"\n"
"QTreeWidget::item:selected {\n"
"    background-color:rgb(40, 105, 254);\n"
"    border-style: inset;\n"
"}\n"
"\n"
"QTreeView::branch {background: transparent;}\n"
"QTreeView::branch:adjoins-item {border-image: url(branch-more.png) 0;}\n"
"QTreeView::branch:!adjoins-item {border-image: url(vline.png) 0;}")


def updataListItem(path,treeWidget):
	"""
	:param path:
	:param TreeWidge: Qt TreeWidge
	:return:
	"""
	def populateTree(treeWidget, path, parentItem):
		for name in os.listdir(path):
			childPath = os.path.join(path, name)
			if os.path.isdir(childPath):
				childItem = QtWidgets.QTreeWidgetItem(parentItem)
				childItem.setText(0, name)
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(pypath + "\img/folder-dynamic-color.png"), QtGui.QIcon.Normal,
							   QtGui.QIcon.Off)

				childItem.setIcon(0, icon)
				populateTree(treeWidget, childPath, childItem)


	treeWidget.clear()
	populateTree(treeWidget, path, treeWidget.invisibleRootItem())

	treeWidgetStyleSheet(treeWidget)
	# return item_dirs


def updataLibraryItem(path,TableWidget,TableWidgetWidth=200):
	global itemWidth
	selected_indexes = TableWidget.selectedIndexes()
	selected_indexes = TableWidget.selectedIndexes()
	for index in selected_indexes:
		selectrow= index.row() + 1
		selectcolumn = index.column() + 1

	#行数*列数+列数
		# selectindex =selectrow*(selectcolumn+1)+selectcolumn+1
		# print(selectrow)
		# print(selectcolumn)


	TableWidget.clear()
	TableWidgetWidth = TableWidgetWidth
	# print(TableWidgetWidth)
	AllItemFrame = []
	itemWidth = itemWidth
	pngfile = file.getfile(path, ".png")

	columnCount = TableWidgetWidth // itemWidth+1 # 列数
	rowCount = len(pngfile) // columnCount			# 行数

	if len(pngfile)%columnCount:
		rowCount+=1
	TableWidget.setRowCount(rowCount)		#设置列数
	TableWidget.setColumnCount(columnCount) 	#设置行数

	itemWidthA = (TableWidgetWidth-20)/(columnCount)		#重新计算itemWidth大小
	# print(itemWidthA)

	for i in range(len(pngfile)):
		row = i // columnCount
		column = i % columnCount

# 		FrameA.setStyleSheet("QFrame {background-color:transparent;")
# 		FrameALayout = QtWidgets.QVBoxLayout(FrameA)
# 		BtnA = QtWidgets.QPushButton(FrameA)
# 		icon_img = QtGui.QIcon()
# 		icon_img.addPixmap(QtGui.QPixmap(pngfile[i]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
# 		BtnA.setIcon(icon_img)
# 		BtnA.setIconSize(QtCore.QSize(60, 60))
# 		#BtnA.setEnabled(False)
# 		BtnA.setStyleSheet("QpushButton {background-color:transparent;")
# 		LineEditA = QtWidgets.QLineEdit(FrameA)
# 		LineEditA.setStyleSheet("QLineEdit{\n"
# "    background-color:transparent;\n"
# "    color:rgb(176, 176, 176);\n"
# "    border-style: outset;\n"
# "    border-width: 0px;\n"
# "    border-radius: 3px;\n"
# "    border-color: beige;\n"
# "    padding: 2px;\n"
# "    text-align:left\n"
# "}\n"
# "")
# 		LineEditText = file.getfileName(pngfile[i])
# 		LineEditA.setText(LineEditText)
# 		LineEditA.setAlignment(QtCore.Qt.AlignCenter)
# 		FrameALayout.addWidget(BtnA)
# 		FrameALayout.addWidget(LineEditA)
		# TableWidget.setCellWidget(row, column, FrameA)
		myWidget = MyWidget(row,column ,TableWidget ,pngfile[i] )
		#myWidget.resize(QtCore.QSize(90,itemWidth))


		# myWidget.label.setPixmap(pixmap)
		# myWidget.label.resize(QtCore.QSize(30, 30))


		icon_img = QtGui.QIcon()
		icon_img.addPixmap(QtGui.QPixmap(pngfile[i]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		myWidget.button.setIcon(icon_img)
		myWidget.button.setIconSize(QtCore.QSize(itemWidthA-30, itemWidthA-30))

		LineEditText = file.getfileName(pngfile[i])
		myWidget.lineEdit.setText(LineEditText)
		myWidget.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

		TableWidget.setCellWidget(row, column, myWidget)
		#设置宽高
		TableWidget.setRowHeight(row,itemWidthA)
		TableWidget.setColumnWidth(column,itemWidthA)
		AllItemFrame.append(myWidget)
		TableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
		myWidget.lineEdit.setReadOnly(False)
		# myWidget.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
		myWidget.lineEdit.setEnabled(False)

	for row in range(TableWidget.rowCount()):
		for column in range(TableWidget.columnCount()):
			if TableWidget.cellWidget(row, column) is None:
				# item = TableWidget.item(row, column)
				# item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
				emptyItem = QtWidgets.QTableWidgetItem()
				emptyItem.setFlags(emptyItem.flags() & ~QtCore.Qt.ItemIsEnabled)
				TableWidget.setItem(row, column, emptyItem)
				TableWidget.setFocusPolicy(QtCore.Qt.NoFocus)  #点击有虚线

	return None

#获取全部item和位置
def itemsort(TableWidget,AllItemFrame):
	TableWidget.clear()
	TableWidgetWidth = TableWidget.width()
	itemWidth = 80

	columnCount = TableWidgetWidth // itemWidth  # 列数
	rowCount = len(AllItemFrame) // columnCount

	if len(AllItemFrame)%columnCount:
		rowCount+=1
	#print(rowCount ,columnCount)
	TableWidget.setRowCount(rowCount)
	TableWidget.setColumnCount(columnCount)
	itemWidth = (TableWidgetWidth-10)/columnCount
	# R = 0
	# C = -1

	for i in range(len(AllItemFrame)):
		row = i // columnCount
		column = i % columnCount
		# print(row,column)
		TableWidget.setCellWidget(row, column, AllItemFrame[i])
		TableWidget.setRowHeight(row, 90)
		TableWidget.setColumnWidth(column, itemWidth)

		# for j in range(rowCount):
		# 	if i ==0
		# 	TableWidget.setCellWidget(i, j, AllItemFrame[i+j])
		#
		# if i %columnCount ==0 and i > columnCount-1:
		# 	R = R+1
		# 	C = 0
		# 	#print("true")
		# elif (columnCount+1)*C+C>len(AllItemFrame):
		# 	break
		# else:
		# 	C = C + 1
		# 	#print(R,C)
		# TableWidget.setCellWidget(R, C,AllItemFrame[i])
		# TableWidget.setRowHeight(R,90)
		# TableWidget.setColumnWidth(C,itemWidth)
		# print(R,C)


	return None



def BtnSetIcons(PushButton,iconsPath):
	icon_img = QtGui.QIcon()
	icon_img.addPixmap(QtGui.QPixmap(iconsPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	PushButton.setIcon(icon_img)
	PushButton.setIconSize(QtCore.QSize(22, 22))
	PushButton.setText("")


def add_child(treeweiget,item=None,name="folder"):
	# Get the current selected item
	current = treeweiget.currentItem()
	if current:
		# Get the number of children
		count = current.childCount()
		# Create a new child item
		child = QtWidgets.QTreeWidgetItem()
		# child.setText(0, f"Child {count + 1}")
		child.setText(0, name)
		# Set the child item to be editable
		child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
		# Add the child item to the current item
		current.addChild(child)

	return child

def get_item_name(item):
	namelist = []
	while item:
		namelist.append(item.text(0))
		item = item.parent()
	path =""
	for i in range(len(namelist)):
		if i ==0 :
			path = namelist[i]
		else:
			path = namelist[i]+"//"+path

	return path
def get_item_path(treeWidget):
	selected_items = treeWidget.selectedItems()
	for item in selected_items:
		path = get_item_name(item)
		# path = path.encode("utf-8").decode("unicode_escape")

	return path