from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.treewidget = MyTreeWidget()
        self.setCentralWidget(self.treewidget)

class MyTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setHeaderLabels(["Column 1"])
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)

    def rightMenuShow(self):
        try:
            rightMenu = QtWidgets.QMenu(self)
            removeAction = rightMenu.addAction(u"删除")
            copyAction = rightMenu.addAction(u"复制")
            renameAction = rightMenu.addAction(u"重命名")
            addChildAction = rightMenu.addAction(u"添加子项")
            action = rightMenu.exec_(QtGui.QCursor.pos())
            if action == removeAction:
                for item in self.selectedItems():
                    index = self.indexOfTopLevelItem(item)
                    if index != -1:
                        self.takeTopLevelItem(index)
            elif action == copyAction:
                text = ""
                for item in self.selectedItems():
                    index = self.indexOfTopLevelItem(item)
                    if index != -1:
                        text += item.text(0) + "\n"
                clipboard = QtWidgets.QApplication.clipboard()
                clipboard.setText(text.strip())
            elif action == renameAction:
                for item in self.selectedItems():
                    index = self.indexOfTopLevelItem(item)
                    if index != -1:
                        dialog = RenameDialog()
                        if dialog.exec_() == QtWidgets.QDialog.Accepted:
                            text = dialog.textValue()
                            if text:
                                item.setText(0, text)
            elif action == addChildAction:
                for item in self.selectedItems():
                    index = self.indexOfTopLevelItem(item)
                    if index != -1:
                        childCount=item.childCount()+1
                        child=QtWidgets.QTreeWidgetItem(["child %s"%childCount])
                        item.addChild(child)

        except Exception as e:
            print(e)

class RenameDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        layout=QtWidgets. QVBoxLayout()
        self.lineedit=QtWidgets. QLineEdit()
        layout.addWidget(self.lineedit)
        buttonBox=QtWidgets. QDialogButtonBox(QtWidgets. QDialogButtonBox.Ok|QtWidgets. QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def textValue(self):
      return 	self.lineedit.text()

if __name__=="__main__":
    app=QtWidgets. QApplication([])
    window=MyWindow()
    for i in range(10):
      item=QtWidgets. QTreeWidgetItem(["item %s"%i])
      window.treewidget.addTopLevelItem(item)
    window.show()
    app.exec_()