# -*- coding: utf-8 -*-
from pymxs import runtime as rt
import pymxs
from PoseLibrary.Maxcommand import cmds as cmds


def savePose():
    """
    :param obj:
    :return:posedata
    """
    objs = cmds.ls()
    posedata = []
    if objs:
        for obj in objs :
            if rt.getPropertyController(obj.controller, 'Horizontal') != None:  #判断是否是质心
                objdata = {}
                objdata["obj"] = str(obj)
                objdata["objtype"] = str(rt.classOf(obj))
                objdata["objname"] = obj.name
                objdata["objtransform"] = str(obj.transform)
                posedata.append(objdata)
            elif rt.classOf(obj) == rt.Biped_Object:    #判断是否是biped类
                objdata = {}
                objdata["obj"] = str(obj)
                objdata["objtype"] = str(rt.classOf(obj))
                objdata["objname"] = obj.name
                objdata["objtransform"] = str(obj.transform)
                posedata.append(objdata)
            else:
                # objtype = rt.classOf(obj.name
                # print(objtype)
                objdata = {}
                objdata["obj"] = str(obj)
                objdata["objtype"] = str(rt.classOf(obj))
                objdata["objname"] = obj.name
                objdata["objtransform"] = str(obj.transform)
                objdata["objposition"] = str(obj.position)
                objdata["objrotation"] = str(obj.rotation)
                objdata["objscale"] = str(obj.scale)
                posedata.append(objdata)
    return posedata



def pastPoseTh(posedata,selectobjs,count,progressBar):
    """
    粘贴pose，对线程模式，count是迭代次数
    :param posedata:
    :param selectobjs:
    :param count:
    :return:
    """
    posedata = posedata
    max = len(posedata)*count
    print(max)
    k = 1
    for i in range(count):
        for data in posedata:
            progressBar.setValue(float(k)/float(max)*100)
            # pymxs rt多线程标准格式
            k = k+1
            with pymxs.mxstoken():
                obj = rt.getNodeByName(data.get('objname'))
                if obj in selectobjs:
                    tm = cmds.data_to_rtMatrix3(data.get('objtransform'))
                    # pymxs rt多线程标准格式
                    with pymxs.mxstoken():
                        obj.transform = tm
                        # obj.rotation = rt.eulerAngles(x, y, z)
                        # obj.pos = rt.point3(x, y, z)
                        # obj.scale = rt.point3(x, y, z)
    return
def pastPose(posedata,selectobjs,count,progressBar):
    """
    粘贴pose，单线程绝对位置模式，count是迭代次数
    :param posedata:
    :param selectobjs:
    :param count:
    :return:
    """
    posedata = posedata
    max = len(posedata)*count
    k = 1
    with pymxs.undo(True):
        for i in range(count):
            for data in posedata:
                progressBar.setValue(float(k)/float(max)*100)
                k = k+1
                obj = rt.getNodeByName(data.get('objname'))
                if obj in selectobjs:
                    mat3 = cmds.data_to_rtMatrix3(data.get('objtransform'))

                    obj.transform = mat3
                    # obj.rotation = rt.eulerAngles(x, y, z)
                    # obj.pos = rt.point3(x, y, z)
                    # obj.scale = rt.point3(x, y, z)
    return

def pastPoseRot(posedata,selectobjs,count,progressBar):
    """
    粘贴pose，单线程非绝对位置模式，count是迭代次数
    :param posedata:
    :param selectobjs:
    :param count:
    :return:
    """
    posedata = posedata
    max = len(posedata)*count
    k = 1
    with pymxs.undo(True):
        for i in range(count):
            for data in posedata:
                progressBar.setValue(float(k)/float(max)*100)
                k = k+1
                obj = rt.getNodeByName(data.get('objname'))
                if obj in selectobjs:
                    # objpar = obj.parent
                    # parmat3 = objpar.transform
                    mat3 = cmds.data_to_rtMatrix3(data.get('objtransform'))#基于世界空间矩阵
                    # localmat3 = mat3*rt.inverse(parmat3)

                    row1 = mat3.row1
                    row2 = mat3.row2
                    row3 = mat3.row3
                    row4 = obj.transform.row4
                    newmat3 = rt.matrix3(row1,row2,row3,row4)
                    # remat3 = rt.XFormMat(mat3,localmat3)
                    obj.transform = newmat3
                    # obj.rotation = rt.eulerAngles(x, y, z)
                    # obj.pos = rt.point3(x, y, z)
                    # obj.scale = rt.point3(x, y, z)
    return

def getselectobjcount(posedata):
    """
    获取数据的物体个数
    :param posedata:
    :return:
    """
    objs = [rt.getNodeByName(data.get('objname')) for data in posedata]
    selectobjcount = len(objs)
    return selectobjcount



#设置关键帧
