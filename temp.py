from pyfbsdk import *
import math

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
