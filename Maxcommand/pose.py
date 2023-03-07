# -*- coding: utf-8 -*-
from pymxs import runtime as rt
import pymxs

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
            objdata = {}
            objdata["obj"] = str(obj)
            objdata["objname"] = obj.name
            # objdata["objtype"] = obj.superclass
            objdata["objtransform"] = str(obj.transform)
            # objdata["objposition"] = obj.position
            # objdata["objrotation"] = obj.rotation
            # objdata["objscale"] = obj.scale
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

def pastPose(posedata,selectobjs):

    posedata = posedata
    for data in posedata:
        obj = rt.getNodeByName(data.get('objname'))
        if obj in selectobjs:
            tm = data_to_rtMatrix3(data.get('objtransform'))
            obj.transform = tm
            # obj.rotation = rt.eulerAngles(x, y, z)
            # obj.pos = rt.point3(x, y, z)
            # obj.scale = rt.point3(x, y, z)
    rt.redrawViews()
    return

def selectobj(posedata):
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
                rt.setKey(obj, frame)