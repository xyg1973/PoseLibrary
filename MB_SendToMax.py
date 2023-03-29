# -*- coding: utf-8 -*-
from pyfbsdk import *
import math
import os
import sys

scene = FBSystem().Scene
currentTake = FBSystem().CurrentTake

startTime = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
endTime = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

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


def get_children(node, types=None):
    if (not types or isinstance(node, types)) and not node.Selected:
        node.Selected = True
    for child in node.Children:
        get_children(child)
    children = ls()
    return children

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


MaxRoot = FBFindModelByLabelName('Root')
a = get_children(MaxRoot)
PlotAnim()
my_documents_path = os.path.expanduser('~/Documents')
exportPath = my_documents_path+"//SendTemp"
ExportSelect(exportPath)
print(a)
print(currentTake.Name)