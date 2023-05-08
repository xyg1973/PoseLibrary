from PySide2 import QtCore, QtGui, QtWidgets
from PySide2 import shiboken2
from pymxs import runtime as rt
import pymxs
from PoseLibrary.temp.Root_Motion import ui_root_motion as ui_root_motion



reload(ui_root_motion)
class Ui_DockWidget(QtWidgets.QDockWidget):
    def __init__(self,parent=None):
        super(Ui_DockWidget, self).__init__(parent)
        self.ui = ui_root_motion.Ui_Frame()
        self.ui.setupUi(self)
        #解决ui显示堆叠问题
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.ui.verticalLayout)
        self.setWidget(self.widget)
        self.stepWindowUi()
        self.creat_contion()
    def stepWindowUi(self):
        self.ui.progressBar.setVisible(False)
        self.ui.groupBox_4.setVisible(False)
        # self.ui.frame_5.setVisible(False)
        # self.ui.frame_3.setVisible(False)



    def creat_contion(self):
        # self.ui.menu_2.clicked.connect(self.showlogUI)
        # self.ui.menu_2.actions(self.showlogUI)
        self.ui.Btn_root_pick.clicked.connect(self.clicked_Btn_root_pick)
        self.ui.Btn_Pelvis_pick.clicked.connect(self.clicked_Btn_Pelvis_pick)
        self.ui.radioBtn_custom_frame.clicked.connect(self.clicked_radioBtn_custom_frame)
        self.ui.radioBtn_current_frame.clicked.connect(self.clicked_radioBtn_custom_frame)
        self.ui.radioButton.clicked.connect(self.clicked_radioBtn_custom_frame)
        self.ui.cBox_posZ.clicked.connect(self.clicked_cBox_posZ)
        self.ui.Btn_frame_end_pick.clicked.connect(self.clicked_Btn_frame_end_pick)
        self.ui.Btn_frame_start_pick.clicked.connect(self.clicked_Btn_frame_start_pick)
        self.ui.Btn_frame_reference_pick.clicked.connect(self.clicked_Btn_frame_reference_pick)
        self.ui.Btn_frame_range_pick.clicked.connect(self.clicked_Btn_frame_range_pick)
        self.ui.Btn_Apply.clicked.connect(self.Apply)

    def clicked_radioBtn_custom_frame(self):
        ischeack = self.ui.radioBtn_custom_frame.isChecked()
        if ischeack:
            self.ui.groupBox_4.setVisible(True)
        else:
            self.ui.groupBox_4.setVisible(False)

    def clicked_cBox_posZ(self):
        pass
        # ischeack = self.ui.cBox_posZ.isChecked()
        # if ischeack:
        #     self.ui.frame_5.setVisible(True)
        # else:
        #     self.ui.frame_5.setVisible(False)

    def clicked_Btn_root_pick(self):
        try:
            obj = rt.selection[0]
        except:
            obj = None
        if obj != None:
            self.ui.lineEdit.setText(str(obj.name))
        else:
            self.ui.lineEdit.setText("")

    def clicked_Btn_Pelvis_pick(self):
        try:
            obj = rt.selection[0]
        except:
            obj = None
        if obj != None:
            self.ui.lineEdit_2.setText(str(obj.name))
        else:
            self.ui.lineEdit_2.setText("")

    def clicked_Btn_frame_start_pick(self):
        self.set_spinBox_current_frame(self.ui.spinBox_frame_start)
        pass

    def clicked_Btn_frame_end_pick(self):
        self.set_spinBox_current_frame(self.ui.spinBox_frame_end)
        pass

    def clicked_Btn_frame_reference_pick(self):
        self.set_spinBox_current_frame(self.ui.spinBox_frame_reference)


    def clicked_Btn_frame_range_pick(self):

        starttime = int(rt.animationRange.start.frame)
        endtime = int(rt.animationRange.end.frame)
        self.ui.spinBox_frame_start.setValue(starttime)
        self.ui.spinBox_frame_end.setValue(endtime)
    def set_spinBox_current_frame(self,spinBox):
        curentframe = int(rt.currentTime.frame)
        spinBox.setValue(curentframe)
        return curentframe


    def get_frame_range(self):
        #获取要执行的时间范围
        isUseCustomFrame = self.ui.radioBtn_custom_frame.isChecked()
        isCurrentFrame = self.ui.radioBtn_current_frame.isChecked()
        if isUseCustomFrame:
            starttime = self.ui.spinBox_frame_start.value()
            endtime = self.ui.spinBox_frame_end.value()
        elif isCurrentFrame:
            currenttimeA = rt.currentTime.frame
            starttime = int(currenttimeA)
            endtime = int(currenttimeA )

        else:
            starttime = int(rt.animationRange.start.frame)
            endtime = int(rt.animationRange.end.frame)
        print(starttime,endtime)
        return (starttime,endtime)

    def Apply_do(self,root,Pelvis,offset = 0):
        #获取质心的位移属性
        Pelvis = Pelvis
        root = root
        #判断物体类型
        poslist = []
        rangetime = self.get_frame_range()
        rt.disableSceneRedraw()
        with pymxs.undo(True):
            with pymxs.animate(True):
                for i in range(rangetime[0], rangetime[1]+1):
                    with pymxs.attime(i):
                        rt.sliderTime = i
                        Pelvispos = Pelvis.transform.pos
                        if self.ui.cBox_posX.isChecked():
                            rootposX = Pelvispos.x
                        else:
                            rootposX = 0
                        if self.ui.cBox_posY.isChecked():
                            rootposY = Pelvispos.y
                        else:
                            rootposY = 0
                        if self.ui.cBox_posZ.isChecked():

                            rootposZ = Pelvispos.z - offset
                            if self.ui.radioBtn_ZAxis_zero.isChecked():
                                if rootposZ<0:
                                    rootposZ = 0
                        else:
                            rootposZ = 0
                        root.pos = rt.point3(rootposX,rootposY,rootposZ)
                        poslist.append(Pelvispos)
        rt.enableSceneRedraw()
        rt.redrawViews()

        return poslist

    def get_Z_Axis_offset(self,root,Pelvis):
        rt.disableSceneRedraw()
        try:
            currenttime = rt.currentTime.frame

            framenum = self.ui.spinBox_frame_reference.value()
            rt.sliderTime = framenum

            offset = Pelvis.transform.pos.z - root.transform.pos.z
            rt.sliderTime = currenttime
        except:
            pass
        rt.enableSceneRedraw()
        rt.redrawViews()
        return offset

    def Apply(self):
        rootname = self.ui.lineEdit.text()
        Pelvisname = self.ui.lineEdit_2.text()

        root = rt.getNodeByName(rootname)
        Pelvis = rt.getNodeByName(Pelvisname)
        if root and Pelvis :
            Z_Axis_offset = self.get_Z_Axis_offset(root,Pelvis)
            self.Apply_do(root,Pelvis,offset=Z_Axis_offset)

def main():
    #rt.resetMaxFile(rt.name('noPrompt'))
    # Cast the main window HWND to a QMainWindow for docking
    # First, get the QWidget corresponding to the Max windows HWND:
    main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())
    # Then cast it as a QMainWindow for docking purposes:
    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)
    w = Ui_DockWidget(parent=main_window) #
    w.setFloating(True)
    w.show()


if __name__ == "__main__":
    main()