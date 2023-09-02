# -*- coding: utf-8 -*-
from pyfbsdk import *
import math
import os
import sys


def ls():
    selectedModels = FBModelList()

    topModel = None  # Search all models, not just a particular branch
    selectionState = True  # Return models that are selected, not deselected
    sortBySelectOrder = True  # The last model in the list was selected most recently
    FBGetSelectedModels(selectedModels, topModel, selectionState, sortBySelectOrder)
    obj = []
    for model in selectedModels:
        obj.append(model)
        model, model.LongName
    return obj
def SaveSelect(path):
    filename = path
    options = FBFbxOptions(False)
    # 只保存选中项，格式为ASCII
    options.UseASCIIFormat = True
    options.SaveSelectedModelsOnly = True
    options.SaveSelectedTakesOnly = True
    # 不保存默认选项
    options.BaseCameras = False
    options.CameraSwitcherSettings = False
    options.CurrentCameraSettings = False
    options.GlobalLightingSettings = False
    options.TransportSettings = False
    # exportModels = FBModelList()
    FBApplication().FileSave(filename ,options)
    # FBApplication().FileExport(filename)
    # FBApplication().FileExportBatch(filename, FBSystem().CurrentTake, batchOptions, exportModels)
def PlotAnim():
    # 对plot all属性进行设置并plot
    lOptions = FBPlotOptions()
    lOptions.PlotAllTakes = False
    lOptions.PlotOnFrame = True
    lOptions.PlotPeriod = FBTime(0, 0, 0, 1)  # 表示首帧
    lOptions.PlotLockedProperties = True
    lOptions.UseConstantKeyReducer = True
    lOptions.ConstantKeyReducerKeepOneKey = True
    FBSystem().CurrentTake.PlotTakeOnSelected(lOptions)  # 使上面的设置生效
def ExportSelect(path):
    filename = path
    batchOptions = FBBatchOptions()
    batchOptions.Overwrite = True
    batchOptions.KeepDummyBones = True
    batchOptions.WriteRate = True
    batchOptions.OutputDirectory = os.path.dirname(path)
    # Get the list of selected models
    selectedModels = FBModelList()
    FBGetSelectedModels(selectedModels)
    app = FBApplication()
    app.FileExportBatch(os.path.basename(path), FBSystem().CurrentTake, batchOptions, selectedModels)

def CreateParentConstraint(parent, child, weight):
    """
    创建父子链接
    """
    ##Set Parent Object
    objParent = parent
    ##Set Child Object
    objChild = child

    ##Create "Parent/Child" Constraint
    for i in range(FBConstraintManager().TypeGetCount()):
        if "Parent/Child" in FBConstraintManager().TypeGetName(i):
            lMyConstraint = FBConstraintManager().TypeCreateConstraint(i)

    # for index, element in enumerate(selected_objects):
    lMyConstraint.ReferenceAdd(0, objChild)
    lMyConstraint.ReferenceAdd(1, objParent)

    # Snap if user desires
    # if offset == True:
    # lMyConstraint.Snap()

    # weight of the constraint
    lMyConstraint.Weight = weight

    ##Activate Constraint
    lMyConstraint.Active = True




sourceCamer = ls()[0]
lCamera1 = FBCamera("Camera_Temp")
lCamera1.Show = True
sourceCamer.Selected = False
lCamera1.Selected = True

m = FBMatrix()
sourceCamer.GetMatrix(m)
lCamera1.SetMatrix(m)
CreateParentConstraint(sourceCamer, lCamera1, 100)
lCamera1.Selected = True
PlotAnim()

exportPath = "F:\SNGame/2023/202302\姜泥格挡反击\Fbx//F1_4021_FightBack_cam"
ExportSelect(exportPath)
