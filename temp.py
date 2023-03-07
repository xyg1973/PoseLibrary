import sys
from PySide2 import QtCore, QtWidgets
from view_cortes2 import Ui_MainWindow

class MainWindow_EXEC(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow_EXEC, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.listWidget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.ui.listWidget:
            if event.type() == QtCore.QEvent.KeyPress:
                key = event.key()
                if key == QtCore.Qt.Key_Return:
                    print("Enter pressed")
                    return True
                elif key == QtCore.Qt.Key_Escape:
                    print("Escape pressed")
                    return True
        return super(MainWindow_EXEC, self).eventFilter(obj, event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_EXEC()
    window.show()
    sys.exit(app.exec_())