# -*- coding: utf-8 -*-
from pyfbsdk import *
import math
import os
import sys
from MobuCore.MobuCoreTools.AdjustmentBlend import AdjustmentBlend as MobuTool_AdjustmentBlend

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


def GetLayerIndex(take, layerVariant):
    '''
    Given a variable representing a layer, returns the index of that layer
    within the given take, or -1 if no such layer exists. layerVariant can
    either be an actual layer object, the name of a layer, or, for the sake of
    convenience, a layer's index.
    '''
    # If the layer variant is already an index, we simply return it
    if isinstance(layerVariant, int):
        return layerVariant

    # Otherwise, we need to qualify it to obtain a name
    if isinstance(layerVariant, basestring):
        name = layerVariant
    else:
        name = layerVariant.Name # It must be an FBAnimationLayer

    # Finally, search for the layer by name
    for i in range(0, take.GetLayerCount()):
        if take.GetLayer(i).Name == name:
            return i
    return -1

def CreateNewLayer(take, name):
    '''
    Creates a new layer in the given take, but conveniently allows an initial
    name to be supplied. Returns the new FBAnimationLayer object.
    '''
    # Puzzlingly, this API method doesn't return the new layer
    take.CreateNewLayer()

    # However, new layers are always created at the top of the stack
    layer = take.GetLayer(take.GetLayerCount() - 1)
    layer.Name = name
    return layer

"""
def SetCurrentLayer(take, layerVariant):
    '''
    Given a variable representing a layer (either an index, a name, or an
    actual layer object), makes that layer current.
    '''
    layerIndex = GetLayerIndex(layerOrName)
    assert layerIndex >= 0

    take.SetCurrentLayer(layerIndex)
    """

def SerializeCurve(fcurve):
    '''
    Returns a list of dictionaries representing each of the keys in the given
    FCurve.
    '''
    keyDataList = []

    for key in fcurve.Keys:
        keyData = {
            'time': key.Time.Get(),
            'value': key.Value,
            'interpolation': int(key.Interpolation),
            'tangent-mode': int(key.TangentMode),
            'constant-mode': int(key.TangentConstantMode),
            'left-derivative': key.LeftDerivative,
            'right-derivative': key.RightDerivative,
            'left-weight': key.LeftTangentWeight,
            'right-weight': key.RightTangentWeight
        }

        keyDataList.append(keyData)

    return keyDataList


def GetObjPosRotCV(obj):
    objAPosX = obj.Translation.GetAnimationNode().Nodes[0].FCurve
    objAPosY = obj.Translation.GetAnimationNode().Nodes[1].FCurve
    objAPosZ = obj.Translation.GetAnimationNode().Nodes[2].FCurve
    objARotX = obj.Rotation.GetAnimationNode().Nodes[0].FCurve
    objARotY = obj.Rotation.GetAnimationNode().Nodes[1].FCurve
    objARotZ = obj.Rotation.GetAnimationNode().Nodes[2].FCurve
    return objAPosX, objAPosY, objAPosZ,objARotX,objARotY,objARotZ


def getObjPosVetor(obj):

    posX = []
    posY = []
    posZ = []
    rotX = []
    rotY = []
    rotZ = []
    objposcv = GetObjPosRotCV(obj)
    print(objposcv)
    objposcvX = SerializeCurve(objposcv[0])
    objposcvY = SerializeCurve(objposcv[1])
    objposcvZ = SerializeCurve(objposcv[2])
    objrotcvx = SerializeCurve(objposcv[3])
    objrotcvy = SerializeCurve(objposcv[4])
    objrotcvz = SerializeCurve(objposcv[5])
    for i in range(len(objposcvX)):
        posX.append(objposcvX[i]['value'])
        posY.append(objposcvY[i]['value'])
        posZ.append(objposcvZ[i]['value'])

        rotX.append(objrotcvx[i]['value'])
        rotY.append(objrotcvy[i]['value'])
        rotZ.append(objrotcvz[i]['value'])

    return posX, posY, posZ, rotX, rotY, rotZ


def getrateA(listA):
    ratelist = []
    for i in range(len(listA)):
        if i == 0:
            pass
        else:
            rateValue = abs(listA[i] - listA[i - 1])
            ratelist.append(rateValue)
    return ratelist


def FrameRate(rate, allabs=0):
    frameratelist = []
    for i in rate:
        val = i / allabs
        frameratelist.append(val)
    return frameratelist


def getallabs(rate):
    val = 0
    for i in rate:
        val = i+val

    return val


def getAddLayoutVal(startVal, endVal, allabs, FrameRate):
    startVal = startVal
    endVal = endVal
    allabs = allabs
    FrameRate = FrameRate
    addallabs = endVal - startVal

    addFarmeVal = [startVal]
    for i in range(len(FrameRate)):
        Val = FrameRate[i] * addallabs + startVal
        startVal = Val

        addFarmeVal.append(Val)
    addFarmeVal.append(endVal)
    return addFarmeVal


def applyBlend(name,startvetor,endvetor):
    ObjPosCV = GetObjPosRotCV(name)
    startTime = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
    endTime = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

    ObjPoslist = getObjPosVetor(name)
    for i in ObjPosCV :
        cvcount = 0
        rate = getrateA(ObjPoslist[cvcount])
        allabs = getallabs(rate)
        Frmaeratelist = FrameRate(rate, allabs)
        addVal = getAddLayoutVal(startvetor[cvcount], endvetor[cvcount], allabs, Frmaeratelist)

        for k in range(startTime, endTime):
            i.KeyAdd(FBTime(0, 0, 0, k), addVal[k])
        cvcount = cvcount+1


def AdjustmentBlend_Apply():
    take = FBSystem().CurrentTake
    objs = ls()
    startTime = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
    endTime = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

    allObjAddLayout_StartVetor = []
    allObjAddLayout_EndVetor = []
    allObjVetor = []

    take.SetCurrentLayer(0)
    for obj in objs:
        take.SetCurrentLayer(0)
        take = FBSystem().CurrentTake
        vetorval = getObjPosVetor(obj)
        take.SetCurrentLayer(1)
        startVetor = getObjPosVetor(obj)
        endvetor = getObjPosVetor(obj)

        allObjVetor.append(vetorval)
        allObjAddLayout_StartVetor.append(startVetor)
        allObjAddLayout_EndVetor.append(endvetor)

    print(allObjAddLayout_StartVetor)
    print(allObjAddLayout_EndVetor)
    print("------------------")
    print(len(allObjVetor))

    alladdVal = []
    for obj in objs:
        objcount = len(objs)
        print(objcount)
        objcv = GetObjPosRotCV(obj)


        count = 0
        for i in range(0, 6):
            print(i)
            rate= getrateA( allObjVetor[objcount-1][i])
            allabs = getallabs(rate)
            Frmaeratelist = FrameRate(rate, allabs)
            startval = allObjAddLayout_StartVetor[objcount-1][i][0]
            endVal = allObjAddLayout_EndVetor[objcount-1][i][1]
            print (startval)
            print(endVal)
            addVal = getAddLayoutVal(startval,endVal ,allabs, Frmaeratelist)
            alladdVal.append(addVal)

            print(objcv[count])
            for k in range(startTime, endTime+1):
                objcv[count].KeyAdd(FBTime(0, 0, 0, k), addVal[k])

            count = count + 1
        objcount= objcount +1
    print(objs)


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


def SN_Send_Select_to_Max():
    MaxRoot = FBFindModelByLabelName('Root')
    a = get_children(MaxRoot)
    PlotAnim()
    my_documents_path = os.path.expanduser('~/Documents')
    exportFolder = my_documents_path+"/SN AnimTool"


    if not os.path.exists(exportFolder):
        # 如果文件夹不存在，则创建它
        os.makedirs(exportFolder)

    exportPath = my_documents_path+"/SN AnimTool/SendTemp_Mb"
    ExportSelect(exportPath)

def Update_Sence():
    my_documents_path = os.path.expanduser('~/Documents')

    file_path =my_documents_path+"/SN AnimTool/SendTemp_Max.fbx"
    app = FBApplication()
    app.FileMerge(file_path)

def AdjustmentBlend():
    objs = ls()
    for obj in objs:
        for comp in FBSystem().Scene.Components:
            comp.Selected = False
        obj.Selected = True
        selecobj = FBModelList()
        topModel = None  # Search all models, not just a particular branch
        selectionState = True  # Return models that are selected, not deselected
        sortBySelectOrder = True  # The last model in the list was selected most recently
        FBGetSelectedModels(selecobj, topModel, selectionState, sortBySelectOrder)
        AdjustmentBlend_Apply()

def menuTestEvent():
    print("test")





def OnMenuClick(eventName):
    if eventName == "Adjustment Blend":
        MobuTool_AdjustmentBlend.AdjustmentBlendCharacter()
    elif eventName == "Test":
        menuTestEvent()
    elif eventName =="Update_Sence":
        Update_Sence()
        print("更新场景")
    elif eventName == "Send_Select_to_max":
        SN_Send_Select_to_Max()
        print("发送到max")
    else:
        FBMessageBox("Error...", "Menu Error: This option hasn't been set up yet. Please contact your friendly neighbourhood Technical Animator", "OK")



def LoadMenu():
    def MenuOptions(control, event):
        eventName = event.Name
        OnMenuClick(eventName)

    mainMenuName = "SN AnimTool"

    menuManager = FBMenuManager()

    menuManager.InsertLast(None, mainMenuName)

    menuManager.InsertLast(mainMenuName,"Rig")  # I'm adding sub-menus here, but you could add a menu option to the first level of the menu by replacing "Seamanship" with the name of the menu/event.
    # menuManager.InsertLast(mainMenuName, "")  # This creates a line break
    menuManager.InsertLast(mainMenuName, "Anim")
    menuManager.InsertLast(mainMenuName + "/Rig", "Test")
    menuManager.InsertLast(mainMenuName + "/Anim", "Adjustment Blend")
    menuManager.InsertLast(mainMenuName, "Update_Sence")
    menuManager.InsertLast(mainMenuName, "Send_Select_to_max")

    # And then this bit of the script adds the created menu to the Mobu tool bar.

    def AddMenu(mainMenuName, subMenuName=""):
        menu = FBMenuManager().GetMenu(mainMenuName + subMenuName)
        if menu:
            menu.OnMenuActivate.Add(MenuOptions)

    AddMenu(mainMenuName)
    AddMenu(mainMenuName + "/Rig")
    AddMenu(mainMenuName + "/Anim")


# This runs everything, or you can drop the script somewhere in your tools folder and just call LoadMenu() in the Mobu startup script.

LoadMenu()