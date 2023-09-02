# -*- coding: utf-8 -*-
from pymxs import runtime as rt
import pymxs
from PoseLibrary.Maxcommand import cmds as cmds
from PoseLibrary.Maxcommand import pose as pose
from PoseLibrary.Maxcommand import render as render
import threading
def saveAnim():
    animdata=[]
    sencetimedata = cmds.get_sence_time_data()
    type_anim = {"type" : "Anim"}
    animdata.append(type_anim)
    animdata.append(sencetimedata)
    rt.disableSceneRedraw()
    for i in range(int(sencetimedata["starttime"]), int(sencetimedata["endtime"]+1)):
        rt.sliderTime = i
        posedata = pose.savePose()
        animdata.append(posedata)
    rt.enableSceneRedraw()
    rt.redrawViews()
    a = rt.isSceneRedrawDisabled()
    # print(a)
    return animdata

def pastAnim(animdata,selectobjs,mysignal,OffsetTime=0,isPastKeyFrame=True):
    try:
        sencetimedata = animdata[0]
        # print(int(sencetimedata["starttime"]),int(sencetimedata["endtime"]))
        max = len(animdata)-1
        k = 1
        rt.disableSceneRedraw()
        selectobjs_set = set(selectobjs)
        # with pymxs.undo(True):
        with pymxs.animate(True):
            for i in xrange(int(sencetimedata["starttime"]), int(sencetimedata["endtime"]+1)):
                posedata = animdata[k]
                del posedata[0]
                progress_value = float(k) / float(max) * 100
                mysignal.progress_signal.emit(progress_value)  # 发送进度信号
                # progressBar.setValue(float(k) / float(max) * 100)
                #pose.pastPose(posedata,selectobjs,count=2,progressBar)
                for data in posedata:
                    obj = rt.getNodeByName(data.get('objname'))
                    if obj in selectobjs_set:
                        if isPastKeyFrame==True:
                            obj_iskeyframe = data.get('iskeyframe')
                            if obj_iskeyframe == True:
                                mat3 = cmds.data_to_rtMatrix3(data.get('objtransform'))
                                with pymxs.attime(i + OffsetTime):
                                    obj.transform = mat3
                        else:
                            mat3 = cmds.data_to_rtMatrix3(data.get('objtransform'))
                            with pymxs.attime(i+OffsetTime):
                                obj.transform = mat3
                k += 1
        rt.enableSceneRedraw()
        rt.redrawViews()
    except Exception as e:
        print(e)
        rt.enableSceneRedraw()
        rt.redrawViews()
def pastAnim_old(animdata,selectobjs,mysignal,OffsetTime=0,isPastKeyFrame=True):
    sencetimedata = animdata[0]
    max = len(animdata)-1
    k = 1
    rt.disableSceneRedraw()
    # with pymxs.undo(True):
    for i in xrange(int(sencetimedata["starttime"]), int(sencetimedata["endtime"]+1)):
        posedata = animdata[k]
        del posedata[0]
        mysignal.progress_signal.emit(float(k) / float(max) * 100)  # 发送进度信号
        # progressBar.setValue(float(k) / float(max) * 100)
        with pymxs.animate(True):
            #pose.pastPose(posedata,selectobjs,count=2,progressBar)
            for data in posedata:
                obj = rt.getNodeByName(data.get('objname'))
                if obj in selectobjs:
                    if isPastKeyFrame==True:
                        obj_iskeyframe = data.get('iskeyframe')
                        if obj_iskeyframe == True:
                            mat3 = cmds.data_to_rtMatrix3(data.get('objtransform'))
                            with pymxs.attime(i + OffsetTime):
                                obj.transform = mat3
                    else:
                        mat3 = cmds.data_to_rtMatrix3(data.get('objtransform'))
                        with pymxs.attime(i+OffsetTime):
                            obj.transform = mat3
        k += 1
    rt.enableSceneRedraw()
    rt.redrawViews()


def getselectobjcount(animdata):
    posedata = animdata[1]
    objs = [rt.getNodeByName(data.get('objname')) for data in posedata]
    selectobjcount = len(objs)
    return selectobjcount