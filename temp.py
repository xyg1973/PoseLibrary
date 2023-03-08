from PyQt5 import QtWidgets

class MyDelegate(QtWidgets.QStyledItemDelegate):
    def editorEvent(self, event, model, option, index):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            print(f'Row: {index.row()}, Column: {index.column()}')
            # 在这里发送信号
        return super().editorEvent(event, model, option, index)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    table = QtWidgets.QTableWidget()
    table.setRowCount(3)
    table.setColumnCount(3)
    for i in range(3):
        for j in range(3):
            table.setItem(i, j, QtWidgets.QTableWidgetItem(f'Item ({i}, {j})'))
    table.setItemDelegate(MyDelegate())
    table.show()
    app.exec_()