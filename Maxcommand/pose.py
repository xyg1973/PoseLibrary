# -*- coding: utf-8 -*-
from pymxs import runtime as rt
import pymxs
# from UI import windowUI


def make_cylinder():
    cyl = rt.Cylinder(radius=10, height=30)
    rt.redrawViews()

    return


def ls():
    allobj = []
    objs = rt.selection
    for obj in objs:
        allobj.append(obj)
    return allobj
def savePose():
    """
    :param obj:
    :return:posedata
    """
    objs = ls()
    posedata = []
    if objs:
        for obj in objs :
            # objtype = rt.classOf(obj.name
            # print(objtype)
            objdata = {}
            objdata["obj"] = str(obj)
            objdata["objname"] = obj.name
            # objdata["objtype"] = obj.superclass
            objdata["objtransform"] = str(obj.transform)
            # objdata["objposition"] = str(obj.position)
            # objdata["objrotation"] = str(obj.rotation)
            # objdata["objscale"] = str(obj.scale)
            posedata.append(objdata)
    return posedata


def render_and_save(width, height, file_path):
    # 设置渲染输出大小
    rt.renderWidth = width
    rt.renderHeight = height

    # 创建一个 Point2 对象
    output_size = rt.Point2(width, height)

    # 渲染当前视图并获取位图
    rendered_image = rt.render(outputSize=output_size)

    # 保存位图
    rendered_image.filename = file_path
    rt.save(rendered_image)
    #关闭预览窗口
    rt.close(rendered_image)

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


def pastPoseTh(posedata,selectobjs,count,progressBar):
    """
    count是迭代次数
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
                    tm = data_to_rtMatrix3(data.get('objtransform'))
                    # pymxs rt多线程标准格式
                    with pymxs.mxstoken():
                        obj.transform = tm
                        # obj.rotation = rt.eulerAngles(x, y, z)
                        # obj.pos = rt.point3(x, y, z)
                        # obj.scale = rt.point3(x, y, z)
    return
def pastPose(posedata,selectobjs,count,progressBar):
    """
    count是迭代次数
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
                    mat3 = data_to_rtMatrix3(data.get('objtransform'))

                    obj.transform = mat3
                    # obj.rotation = rt.eulerAngles(x, y, z)
                    # obj.pos = rt.point3(x, y, z)
                    # obj.scale = rt.point3(x, y, z)
    return

def pastPoseRot(posedata,selectobjs,count,progressBar):
    """
    count是迭代次数
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


                    mat3 = data_to_rtMatrix3(data.get('objtransform'))
                    row1 = mat3.row1
                    row2 = mat3.row2
                    row3 = mat3.row3
                    row4 = obj.transform.row4
                    newmat3 = rt.matrix3(row1,row2,row3,row4)
                    # remat3 = rt.XFormMat(parmat3,newmat3)

                    obj.transform = newmat3
                    # obj.rotation = rt.eulerAngles(x, y, z)
                    # obj.pos = rt.point3(x, y, z)
                    # obj.scale = rt.point3(x, y, z)
    return
def reViews():
    rt.redrawViews()
def getselectobjcount(posedata):
    objs = [rt.getNodeByName(data.get('objname')) for data in posedata]
    selectobjcount = len(objs)
    return selectobjcount
def selectobj(posedata):
    with pymxs.undo(True):
        objs = [rt.getNodeByName(data.get('objname')) for data in posedata]
        selectobjs = [obj for obj in objs if obj in rt.objects] #获取场景所有物体
        rt.select(selectobjs)
    rt.redrawViews()
    return selectobjs

#设置关键帧
def set_transform_keyframes(objects, frame=rt.sliderTime.frame):
    for obj in objects:
        for prop in ['pos', 'rotation', 'scale']:
            controller = getattr(obj.controller, prop)
            if controller.isKeyable:
                rt.setKeyMode(rt.name(prop))
                rt.setKey