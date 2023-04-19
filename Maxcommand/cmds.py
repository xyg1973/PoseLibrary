# -*- coding: utf-8 -*-
from pymxs import runtime as rt
import pymxs


def ls():
    allobj = []
    objs = rt.selection
    for obj in objs:
        allobj.append(obj)
    return allobj


def selectobj(posedata):

    with pymxs.undo(True):
        rt.clearSelection()
        objs = [rt.getNodeByName(data.get('objname')) for data in posedata]
        selectobjs = [obj for obj in objs if obj in rt.objects] #获取场景所有物体
        rt.select(selectobjs)
    rt.redrawViews()
    return selectobjs

def selectobj_anim(animdata):

    with pymxs.undo(True):
        rt.clearSelection()
        objs = []
        selectobjs=[]
        for data in animdata[1]:
            obj = rt.getNodeByName(data.get('objname'))
            objs.append(obj)
        for objA in objs:
            if objA in rt.objects:
                selectobjs.append(objA)
        rt.select(selectobjs)
    rt.redrawViews()
    return selectobjs
def set_transform_keyframes(objects, frame=rt.sliderTime.frame):
    for obj in objects:
        for prop in ['pos', 'rotation', 'scale']:
            controller = getattr(obj.controller, prop)
            if controller.isKeyable:
                rt.setKeyMode(rt.name(prop))
                rt.setKey

def data_to_rtMatrix3(transform):
    s = transform
    s = s[s.find("["):s.rfind("]") + 1]
    result = eval(s.replace("] [", "], ["))
    p1 = rt.Point3(*result[0])
    p2 = rt.Point3(*result[1])
    p3 = rt.Point3(*result[2])
    p4 = rt.Point3(*result[3])
    Matrix = rt.Matrix3(p1, p2, p3, p4)
    return Matrix

def data_to_rtPoint3(transform):
    s = transform
    s = s[s.find("["):s.rfind("]") + 1]
    result = eval(s.replace("] [", "], ["))
    p1 = rt.Point3(*result[0])
    p2 = rt.Point3(*result[1])
    p3 = rt.Point3(*result[2])
    Point3 = rt.Point3(p1, p2, p3)
    return Point3
def get_sence_time_data():
    sence_time_data = {}
    sence_time_data["starttime"] = rt.animationRange.start.frame
    sence_time_data["endtime"] = rt.animationRange.end.frame
    sence_time_data["currenttime"] = rt.currentTime.frame


    return sence_time_data

