# -*- coding: utf-8 -*-
# Name:IncrementSave
# Hint:
# http://umezo.hatenablog.jp/entry/20100411/1270989691
# http://docs.autodesk.com/MB/2014/ENU/MotionBuilder-SDK-Documentation/index.html?url=files/GUID-FE8DB4BD-ED47-47CD-9439-A31A7ADE565A.htm,topicNumber=d30e8551
# http://docs.python.jp/2/library/os.path.html
# http://qiita.com/CORDEA/items/ee44799e5d029ce3aaac
# http://python.civic-apps.com/file-timestamp/
# http://docs.python.jp/2/library/datetime.html

from pyfbsdk import *
from pyfbsdk_additions import *

import os
import shutil
import datetime

lFileName = FBApplication().FBXFileName
print
os.path.dirname(lFileName)


def FindIncFolder(path):
    returnVal = ""
    if not os.path.isdir(path + "\\old"):
        os.mkdir(path + "\\old")
    returnVal = path + "\\old"
    return returnVal


def FindRelatedFolders(path, name):
    returnVal = []
    name = name.split(".fbx")[0]
    for obj in os.listdir(path):
        if obj == name + ".bck" or obj == name + ".fbm":
            returnVal.append(obj)
    return returnVal


def BackUp(fileName, incName, fromPath, toPath):
    returnVal = True
    errorPath = ""
    # copy related folders
    folderList = FindRelatedFolders(fromPath, fileName)
    for obj in folderList:
        newName = obj.replace(".", "_" + incName + ".")
        if not os.path.exists(toPath + "\\" + newName):
            shutil.copytree(fromPath + "\\" + obj, toPath + "\\" + newName)
        else:
            returnVal = False
            errorPath = errorPath + "\n" + newName
    # copy file
    newFileName = fileName.replace(".", "_" + incName + ".")
    if not os.path.exists(toPath + "\\" + newFileName):
        shutil.copy(fromPath + "\\" + fileName, toPath + "\\" + newFileName)
    else:
        returnVal = False
        errorPath = errorPath + "\n" + newFileName
    if not returnVal:
        FBMessageBox("Error",
                     "Already exist\n" + errorPath + "\n\nCheck backup folder\nor backup by hand\n\nThere is NOT also normal SAVE",
                     "OK")
    return returnVal


def SaveFile(lFileName):
    filePath = os.path.dirname(lFileName)
    fileName = os.path.basename(lFileName)
    fileTime = datetime.datetime.fromtimestamp(os.stat(lFileName).st_mtime)
    fileTime = fileTime.strftime("%Y-%m%d-%H%M-%S")
    incFolderPath = FindIncFolder(filePath)
    if BackUp(fileName, fileTime, filePath, incFolderPath):
        FBApplication().FileSave(lFileName)


def CheckFile():
    lFileName = FBApplication().FBXFileName
    if lFileName == "":
        pass
    else:
        SaveFile(lFileName)


CheckFile()