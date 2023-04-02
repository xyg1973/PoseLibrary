from pymxs import runtime as rt
import pymxs


def ls():
    allobj = []
    objs = rt.selection
    for obj in objs:
        allobj.append(obj)
    return allobj


b = ls()[0]
b.transform = rt.Matrix3(1)
