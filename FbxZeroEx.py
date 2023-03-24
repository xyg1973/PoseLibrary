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


