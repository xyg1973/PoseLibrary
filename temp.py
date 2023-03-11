import os
from PySide2 import QtWidgets,QtCore

def populateTree(treeWidget, path, parentItem):
    for name in os.listdir(path):
        childPath = os.path.join(path, name)
        if os.path.isdir(childPath):
            childItem = QtWidgets.QTreeWidgetItem(parentItem)
            childItem.setText(0, name)
            childItem.setIcon(0, treeWidget.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
            childItem.setData(0, QtCore.Qt.UserRole, childPath)
            populateTree(treeWidget, childPath, childItem)

class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(TreeWidget, self).__init__(parent)
        self.setHeaderLabel('Directory')
        self.itemChanged.connect(self.handleItemChanged)

    def setPath(self, path):
        self.clear()
        populateTree(self, path, self.invisibleRootItem())

    def handleItemChanged(self, item):
        oldPath = item.data(0, QtCore.Qt.UserRole)
        newPath = os.path.join(os.path.dirname(oldPath), item.text(0))
        try:
            os.rename(oldPath,newPath)
            item.setData(0 ,QtCore.Qt.UserRole,newPath)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    tree = TreeWidget()
    tree.setPath('F:\Myself\cache\FASSSSSSSS')
    tree.show()
    app.exec_()