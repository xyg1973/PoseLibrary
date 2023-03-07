# -*- coding: utf-8 -*-
import sys
import os
from PySide2 import QtCore, QtGui, QtWidgets
from Tools import file

pypath = ""


class MyWidget(QtWidgets.QWidget):
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

		# 安装事件过滤器
		self.installEventFilter(self)
		self.button.installEventFilter(self)
		self.lineEdit.installEventFilter(self)

	# 信号事件选中item中部件会同时选中item
	def eventFilter(self, watched,event ):
		if event.type() == QtCore.QEvent.MouseButtonPress:
			self.table_widget.setCurrentCell(self.row,self.column )
			item = self.table_widget.item(self.row,self.column )
			self.table_widget.setItemSelected(item,True )
			return True
		return super(MyWidget,self ).eventFilter(watched,event )


if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	window = QtWidgets.QMainWindow()
	tableWidget = QtWidgets.QTableWidget(4 ,4 ,window )
	window.setCentralWidget(tableWidget)

def updataListItem(path,TreeWidge):
	global pypath
	"""

	:param path:
	:param TreeWidge: Qt TreeWidge
	:return: TreeWidgeItem dirs
	"""
	path = unicode(path)  #加上unicode防止乱码
	force_list = file.getforce(path)
	print(force_list)
	item_dirs = {}  # 创建的treeweiget_item字典

	for i in range(len(force_list)):
		part_force = os.path.abspath(force_list[i] + '\..')  # 父目录
		force_name = force_list[i][len(part_force) + 1:]  # 文件夹名字,方法：文件路径通过切片操作，从开始切去父目录+1的长度，得到文件夹名字
		#print(force_name)
		item = QtWidgets.QTreeWidgetItem([force_name])  # 创建item
		icon5 = QtGui.QIcon()
		icon5.addPixmap(QtGui.QPixmap(pypath+"\img/folder-dynamic-color.png"), QtGui.QIcon.Normal,
						QtGui.QIcon.Off)
		item.setIcon(0, icon5)

		# 创建第一个item
		if i == 0:
			item_dirs[force_list[i]] = item  # 记录创建的item，加入字典item_dirs
			TreeWidge.addTopLevelItem(item)


		else:
			# 如果父目录和项目路径相同
			if path == part_force:
				item_dirs[force_list[i]] = item  # 记录创建的item，加入字典item_dirs
				TreeWidge.addTopLevelItem(item)
			# 如果父目录和项目路径不同
			else:
				# 如果父目录已经创建item
				if part_force in item_dirs:
					# 获取父目录的item,把item设置为子对象
					part_item = item_dirs.get(part_force)
					part_item.addChild(item)
					############################
					item_dirs[force_list[i]] = item  # 记录创建的item，加入字典item_dirs
					TreeWidge.addTopLevelItem(item)

				# 如果父目录还没有创建item
				else:
					item_dirs[force_list[i]] = item  # 记录创建的item，加入字典item_dirs
					TreeWidge.addTopLevelItem(item)
				# print(item_dirs)
				# print("创建根目录2")

	# 创建的treeweiget_item字典保存到list.json文件中

	fileA = open(path + '\\' + 'list.json', 'w')
	# print (file)
	fileA.close()
	fileptch = path + '\\' + 'list.json'

	#data = json.dumps(force_list)
	#with open(fileptch, 'w') as f:
	#	json.dump(force_list, f)
	# print item_dirs

	itemfrist = item_dirs[force_list[0]]
	itemfrist.setSelected(True)

	return item_dirs


def updataLibraryItem(path,TableWidget,TableWidgetWidth=200):
	TableWidget.clear()
	TableWidgetWidth = TableWidgetWidth
	print(TableWidgetWidth)
	AllItemFrame = []
	itemWidth = 80
	pngfile = file.getfile(unicode(path), ".png")

	columnCount = TableWidgetWidth // itemWidth  # 列数
	rowCount = len(pngfile) // columnCount+1			# 行数

	if len(AllItemFrame)%columnCount:
		rowCount+=1

	TableWidget.setRowCount(rowCount)		#设置列数
	TableWidget.setColumnCount(columnCount) 	#设置行数
	itemWidth = (TableWidgetWidth-45)/(columnCount-1)		#重新计算itemWidth大小
	print(itemWidth)

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
		myWidget.button.setIconSize(QtCore.QSize(65, 65))
		#BtnA.setEnabled(False)
		#myWidget.button.setStyleSheet("QpushButton {background-color:transparent;")
# 		myWidget.lineEdit.setStyleSheet("QLineEdit{\n"
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

		# myWidget.label.setPixmap(myWidget.Pixmap.scaled(itemWidth - 300 ,-210))
		LineEditText = file.getfileName(pngfile[i])
		myWidget.lineEdit.setText(LineEditText)
		# myWidget.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

		TableWidget.setCellWidget(row, column, myWidget)
		#设置宽高
		TableWidget.setRowHeight(row,90)
		TableWidget.setColumnWidth(column,itemWidth)
		AllItemFrame.append(myWidget)
		TableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
		myWidget.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
		eventlist = myWidget.eventFilter

	for row in range(TableWidget.rowCount()):
		for column in range(TableWidget.columnCount()):
			if TableWidget.cellWidget(row, column) is None:
				emptyItem = QtWidgets.QTableWidgetItem()
				emptyItem.setFlags(QtCore.Qt.ItemIsEnabled)
				TableWidget.setItem(row, column, emptyItem)
				TableWidget.setFocusPolicy(QtCore.Qt.NoFocus)  #点击有虚线



	return eventlist

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


def add_child(treeweiget):
	# Get the current selected item
	current = treeweiget.currentItem()
	if current:
		# Get the number of children
		count = current.childCount()
		# Create a new child item
		child = QtWidgets.QTreeWidgetItem()
		# child.setText(0, f"Child {count + 1}")
		child.setText(0, "未命名文件夹")
		# Set the child item to be editable
		child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
		# Add the child item to the current item
		current.addChild(child)

	return child