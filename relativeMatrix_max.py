# -*- coding: utf-8 -*-
from pymxs import runtime as rt
import pymxs


def getOffsetMatrix(Pmat,Cmat):
	Pmat = Pmat
	Cmat = Cmat
	offsetMatrix = rt.inverse(Pmat*rt.inverse(Cmat))
	#localMatrix = rt.inverse(Nmat)*Pmat
	return offsetMatrix

def ls():
    allobj = []
    objs = rt.selection
    for obj in objs:
        allobj.append(obj)
    return allobj



#记录偏移矩阵
def saveOffsetMatrix():
    selectobj = ls()
    if len(selectobj)>=2 :
        parentobj = selectobj[0]
