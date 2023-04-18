# -*- coding: utf-8 -*-
from pymxs import runtime as rt
import pymxs
from PoseLibrary.Maxcommand import cmds as cmds
from PoseLibrary.Maxcommand import pose as pose
from PoseLibrary.Maxcommand import render as render
def saveAnim():
    animdata=[]
    sencetimedata = cmds.get_sence_time_data()
    animdata.append(sencetimedata)
    rt.disableSceneRedraw()
    for i in range(int(sencetimedata["starttime"]), int(sencetimedata["endtime"]+1)):
        rt.sliderTime = i
        posedata = pose.savePose()
        animdata.append(posedata)
    rt.enableSceneRedraw()
    rt.redrawViews()
    a = rt.isSceneRedrawDisabled()
    print(a)
    return animdata


def pastAnim(animdata,selectobjs,progressBar):
    sencetimedata = animdata[0]
    max = len(animdata)-1
    print(sencetimedata)
    k = 1
    rt.disableSceneRedraw()
    with pymxs.undo(True):
        for i in range(int(sencetimedata["starttime"]), int(sencetimedata["endtime"]+1)):
            posedata = animdata[k]
            progressBar.setValue(float(k) / float(max) * 100)
            with pymxs.animate(True):
                #pose.pastPose(posedata,selectobjs,count=2,progressBar)
                for data in posedata:
                    obj = rt.getNodeByName(data.get('objname'))
                    if obj in selectobjs:
                        mat3 = cmds.data_to_rtMatrix3(data.get('objtransform'))
                        with pymxs.attime(i):
                            obj.transform = mat3
            k += 1
    rt.enableSceneRedraw()
    rt.redrawViews()


def getselectobjcount(animdata):
    posedata = animdata[1]
    objs = [rt.getNodeByName(data.get('objname')) for data in posedata]
    selectobjcount = len(objs)
    return selectobjcount