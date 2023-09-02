# -*- coding: utf-8 -*-
import os
from PySide2 import QtCore, QtGui, QtWidgets
from SN_AnimTool.tools.PoseLibrary.Tools import file as file
from SN_AnimTool.tools.PoseLibrary.Maxcommand import pose as pose
from SN_AnimTool.tools.PoseLibrary.Maxcommand import cmds as cmds
import json




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
		# self.button .setFocusPolicy(QtCore.Qt.NoFocus)
		self.button.setStyleSheet("QPushButton {\n"
										"    background-color:rgb(53, 53, 53);\n"
										"    color: rgb(225, 225, 225);\n"
										"    border-width: 0px;\n"
										"    border-radius: 3px;\n"
								  		
										"    border-color: rgb(225, 225, 225);\n"
										"    padding: 2px;\n"
										"\n"
										"}\n"
										"QPushButton:hover {\n"
										"    background-color:rgb(68, 68, 68);\n"
										"}\n"
										"QPushButton:pressed {\n"
										"    background-color: rgb(38, 38, 38);\n"
										"    border-style: inset;\n"
										"}\n"
										"")
		# pixmap = QtGui.QPixmap(pngpath)
		# pixmap.scaled(40, 40)
		# self.label.setPixmap(pixmap)
		# self.label.resize(QtCore.QSize(40,40))
		self.button_type = QtWidgets.QPushButton()
		# self.button_type.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_type.setMaximumHeight(3)
		self.button_type.setEnabled(False)
		#rgb(225, 70, 70)
		self.button_type.setStyleSheet("QPushButton {\n"
								  "    background-color:rgb(140, 140, 140);\n"
								  "    color: rgb(225, 225, 225);\n"
								  "    border-width: 0px;\n"
								  "    border-radius: 3px;\n"
								  "    border-color: beige;\n"
								  "    padding: 2px;\n"
								  "\n"
								  "}\n"
								  "QPushButton:hover {\n"
								  "    background-color:rgb(225, 225, 225);\n"
								  "}\n"
								  "QPushButton:pressed {\n"
								  "    background-color: rgb(225, 225, 225);\n"
								  "    border-style: inset;\n"
								  "}\n"
								  "")
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
		self.layout.addWidget(self.button_type)
		self.layout.addWidget(self.lineEdit)

		self.layout.setSpacing(0)
		#self.layout.setContentsMargins(0, 0, 0, 0)
		#安装事件过滤器
		self.installEventFilter(self)
		self.button.installEventFilter(self)
		self.button_type.installEventFilter(self)
		# self.lineEdit.installEventFilter(self)

	# 信号事件选中item中部件会同时选中item


	def eventFilter(self, watched,tableweigetevent ):

		if tableweigetevent.type() == QtCore.QEvent.MouseButtonPress:
			global JSONPATH
			self.table_widget.setCurrentCell(self.row,self.column )
			item = self.table_widget.item(self.row,self.column )
			self.table_widget.setItemSelected(item,True )

			return True

		#双击事件
		if tableweigetevent.type() == QtCore.QEvent.MouseButtonDblClick:
			global JSONPATH
			try:
				from SN_AnimTool.tools.PoseLibrary.UI import windowUI as windowUI

				JSONPATH = windowUI.JSONPATH
			except:
				pass
			JSONPATH =  windowUI.JSONPATH

			try:
				with open(JSONPATH) as f:
					# 使用 readlines() 读取所有行并储存在列表中
					lines = f.readlines()
					# 获取第2行（索引从0开始，因此需要使用索引1来获取第2行）
					type_text = lines[1].strip() + lines[2].strip() + lines[3].strip()

				type_text = type_text[:-1]
				type_text = eval(type_text)
				file_type = type_text.get("type")
				if file_type == "Pose":
					with open(JSONPATH, 'r') as file:
						posedata = json.load(file)
					objs = cmds.selectobj(posedata)
					if objs ==[]:
						msg = QtWidgets.QMessageBox.information(self, "PoseLibrary消息",
																"\n场景内没有找到数据中的物体\n",
																QtWidgets.QMessageBox.Ok)
				elif file_type == "Anim":
					with open(JSONPATH, 'r') as file:
						animdata = json.load(file)
					objs = cmds.selectobj_anim(animdata)
					if objs ==[]:
						msg = QtWidgets.QMessageBox.information(self, "PoseLibrary消息",
																"\n场景内没有找到数据中的物体\n",
																QtWidgets.QMessageBox.Ok)
			except Exception as e:
				print(e)


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
"background-color:rgb(68, 68, 68);\n"
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
"\n")


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
				current_path = os.path.dirname(os.path.abspath(__file__))
				parent_dir = os.path.dirname(current_path)
				icons_path = parent_dir + "//res//icons"
				icon.addPixmap(QtGui.QPixmap(icons_path + "/folder-dynamic-color.png"), QtGui.QIcon.Normal,
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
	TableWidget.clear()
	TableWidgetWidth = TableWidgetWidth
	# print(TableWidgetWidth)
	AllItemFrame = []
	itemWidth = itemWidth
	pngfile = file.getfile(path, ".png")
	jsonfile = file.getfile(path, ".json")
	columnCount = TableWidgetWidth // itemWidth+1 # 列数
	rowCount = len(pngfile) // columnCount			# 行数

	if len(pngfile)%columnCount:
		rowCount+=1
	TableWidget.setRowCount(rowCount)		#设置列数
	TableWidget.setColumnCount(columnCount) 	#设置行数

	itemWidthA = (TableWidgetWidth-40)/(columnCount)		#重新计算itemWidth大小
	# print(itemWidthA)

	for i in range(len(pngfile)):
		row = i // columnCount
		column = i % columnCount

		myWidget = MyWidget(row,column ,TableWidget ,pngfile[i] )
		icon_img = QtGui.QIcon()
		icon_img.addPixmap(QtGui.QPixmap(pngfile[i]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		myWidget.button.setIcon(icon_img)
		myWidget.button.setIconSize(QtCore.QSize(itemWidthA-30, itemWidthA-30))

		LineEditText = file.getfileName(pngfile[i])
		# print(LineEditText)
		myWidget.lineEdit.setText(LineEditText)
		myWidget.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

		TableWidget.setCellWidget(row, column, myWidget)
		#设置宽高
		TableWidget.setRowHeight(row,itemWidthA)
		TableWidget.setColumnWidth(column,itemWidthA)
		AllItemFrame.append(myWidget)
		# TableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
		myWidget.lineEdit.setReadOnly(False)
		# myWidget.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
		myWidget.lineEdit.setEnabled(False)
		#判断数据类型：
		try:
			with open(jsonfile[i]) as f:
				# 使用 readlines() 读取所有行并储存在列表中
				lines = f.readlines()
				# 获取第2行（索引从0开始，因此需要使用索引1来获取第2行）
				type_text = lines[1].strip()+lines[2].strip()+lines[3].strip()

			type_text = type_text[:-1]
			type_text = eval(type_text)
			file_type = type_text.get("type")
			if file_type == "Pose":
				myWidget.button_type.setStyleSheet("QPushButton {\n"
												   "    background-color:rgb(140, 140, 140);\n"
												   "    color: rgb(225, 225, 225);\n"
												   "    border-width: 0px;\n"
												   "    border-radius: 3px;\n"
												   "    border-color: beige;\n"
												   "    padding: 2px;\n"
												   "\n"
												   "}\n"
												   "QPushButton:hover {\n"
												   "    background-color:rgb(225, 225, 225);\n"
												   "}\n"
												   "QPushButton:pressed {\n"
												   "    background-color: rgb(225, 225, 225);\n"
												   "    border-style: inset;\n"
												   "}\n"
												   "")
				# print("这是pose类型")
			elif file_type =="Anim":
				myWidget.button_type.setStyleSheet("QPushButton {\n"
												   "    background-color:rgb(225, 140, 140);\n"
												   "    color: rgb(225, 225, 225);\n"
												   "    border-width: 0px;\n"
												   "    border-radius: 3px;\n"
												   "    border-color: beige;\n"
												   "    padding: 2px;\n"
												   "\n"
												   "}\n"
												   "QPushButton:hover {\n"
												   "    background-color:rgb(225, 225, 225);\n"
												   "}\n"
												   "QPushButton:pressed {\n"
												   "    background-color: rgb(225, 225, 225);\n"
												   "    border-style: inset;\n"
												   "}\n"
												   "")
		except Exception as e:
			pass
			# print(e)

	#隐藏点击虚线
	for row in range(TableWidget.rowCount()):
		for column in range(TableWidget.columnCount()):
			if TableWidget.cellWidget(row, column) is None:
				# item = TableWidget.item(row, column)
				# item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
				emptyItem = QtWidgets.QTableWidgetItem()
				emptyItem.setFlags(emptyItem.flags() & ~QtCore.Qt.ItemIsEnabled)
				TableWidget.setItem(row, column, emptyItem)
				# TableWidget.setFocusPolicy(QtCore.Qt.NoFocus)  #点击有虚线



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



def BtnSetIcons(PushButton,iconsPath,Text = "",size = 18):
	icon_img = QtGui.QIcon()
	icon_img.addPixmap(QtGui.QPixmap(iconsPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	PushButton.setIcon(icon_img)
	PushButton.setIconSize(QtCore.QSize(size, size))
	PushButton.setText(Text)


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
		# child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
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