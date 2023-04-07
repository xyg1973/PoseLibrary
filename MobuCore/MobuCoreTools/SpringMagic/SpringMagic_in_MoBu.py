# -*- coding: utf-8 -*-
# Spring Magic in MB

# A chain motion calculate script for Motion Builder, tested at MB 2014 and newer
# Similar function with same name tool in 3DsMax
# Only support +x towards child bone mode

# special thanks: Kartik

# Yanbin Bai
# 2021.02
# baiyanbin@outlook.com

# Version history:

# 2.1
# make progress bar work

# 2.0
# add pose match

# 1.9
# add inertia effect

# 1.8
# bake animation according to playback frame rate setting

# 1.7
# fix bug that bind controller cannot working correctly if source bone has scaling
# add select branch button

# 1.6
# fix bug on bind controller axis

# 1.5
# add bind and bake controller function
# UI adjustment

# 1.4
# improve twist
# add Flex
# add Wind

# 1.3
# improve performance
# add tension

# 1.2
# improve spring algorithm to reduce popping
# performance optimization, about 2 times faster
# improve collision algorithm

# 1.1
# add collision system

# 1.0
# first working version





from pyfbsdk import *
from pyfbsdk_additions import *
import webbrowser
import os
import math
import base64
import urllib2
import datetime
# print "acos",math.acos(10)

version = 2.1
url = r"http://animbai.com"
email = r'baiyanbin@outlook.com'
capsuleSubFix = '_ColBody'
windConeName = 'SpringMagic_WindCone'

spring_lable = FBLabel()
spring_edit = FBEditNumber()
twist_lable = FBLabel()
twist_edit = FBEditNumber()
tension_lable = FBLabel()
tension_edit = FBEditNumber()
mass_lable = FBLabel()
mass_edit = FBEditNumber()
flex_lable = FBLabel()
flex_edit = FBEditNumber()
subDiv_lable = FBLabel()
subDiv_edit = FBEditNumber()
loop_button = FBButton()
poseMatch_button = FBButton()
range_lable = FBLabel()
range_button = FBButton()
straightBone_button = FBButton()
copyBone_button = FBButton()
pasteBone_button = FBButton()
branch_button = FBButton()
apply_button = FBButton()
bone_lable = FBLabel()
ver_lable = FBLabel()
local_lable = FBLabel()
Author_button = FBButton()
wind_button = FBButton()
addBody_button = FBButton()
deleteBody_button = FBButton()
removeAllBody_button = FBButton()
capsule_lable = FBLabel()
collision_button = FBButton()
collision_fast_button = FBButton()
ctrl_lable = FBLabel()
ctrlBind_button = FBButton()
ctrlBake_button = FBButton()


boneMatrixDict = {}

nullSubFix = '_SpringNull'

proxySubFix = '_ChainProxy'
consSubFix = '_ChainConstraint'

versionCheckLink = r'http://animbai.com/springmagicinmobuver/'

def BtnCallbackstraightBone_button(control, event):
    straightBone()

def BtnCallbackcopyBone_button(control, event):
    copyBone()

def BtnCallbackpasteBone_button(control, event):
    pasteBone()

def BtnCallbackbranch_button(control, event):
    selectBranchBone()

def BtnCallbackapply_button(control, event):
    main()

def BtnCallbackAuthor_button(control, event):
    # open linked in page
    webbrowser.open(url,new=2)

def BtnCallbackaddBody_button(control, event):
    addBody()

def BtnCallbackdeleteBody_button(control, event):
    deleteBody()

def BtnCallbackremoveAllBody_button(control, event):
    deleteBody(isClear=True)

def BtnCallbackwind_button(control, event):
    addWindCone()

def BtnCallbackctrlBind_button(control, event):
    ctrlBind()

def BtnCallbackctrlBake_button(control, event):
    ctrlBake()

def checkUpdate():

    page_source = None

    try:
        page_source = urllib2.urlopen(versionCheckLink, timeout = 5).read()
    except:
        pass

    if page_source:
        new_version = float(page_source.split('|version|')[1])

        # if new_version > version:
        #     miscUpdate_button.setVisible(1)
        spam_word=[]

        spam_word.append(page_source.split('|spam1|')[1])
        spam_word.append(page_source.split('|spam2|')[1])
        spam_word.append(page_source.split('|spam3|')[1])

        # print spam_word

def creatConstraint(consName):
    # consName = 'help' will return all constraint name
    cons = None

    m = FBConstraintManager()
    count = m.TypeGetCount()

    consNameDict = {}
    for i in range(count):
        consNameRef = m.TypeGetName(i)
        consNameDict[consNameRef] = i

    if consName in consNameDict.keys():
        cons = m.TypeCreateConstraint( consNameDict[consName] )

    if consName == 'help':
        cons = consNameDict.keys()

    return cons

def GetObjByType( lType ):
    # get objects by type
    # lType could be FBTake_TypeInfo(), FBCamera_TypeInfo(), FBSet_TypeInfo() and etc
    lTypedCompList = []
    for lComp in FBSystem().Scene.Components:
        if lComp.Is( lType ):
            lTypedCompList.append( lComp )
    return lTypedCompList

def PrintProperty( pModel ):
    lPropMgr = pModel.PropertyList
    for lProp in lPropMgr:
        print lProp.GetName()

def selectBranchBone():
    objs = FBModelList()
    FBGetSelectedModels( objs )
    if len(objs)>0:
        SelectBranch(objs[0])
    # objs[0].Selected = False
    # objs[0].Selected = True

def SelectBranch(topModel):
    '''
    Selects the given model and all of its descendants. Note that this
    function does not clear the current selection -- that's the caller's
    responsibility, if desired.
    '''
    topModel.Selected = True
    for childModel in topModel.Children:
        SelectBranch(childModel)


def AlignTR( pModel, pAlignTo ):

   lAlignTransPos = FBVector3d()
   lModelTransPos = FBVector3d()
   lAlignRotPos = FBVector3d()
   lModelRotPos = FBVector3d()
   
   pAlignTo.GetVector(lAlignTransPos)
   pModel.GetVector(lModelTransPos)

   pAlignTo.GetVector(lAlignRotPos, FBModelTransformationType.kModelRotation )
   pModel.GetVector(lModelRotPos, FBModelTransformationType.kModelRotation)

   pModel.SetVector(lAlignTransPos)
   pModel.SetVector(lAlignRotPos, FBModelTransformationType.kModelRotation)

def ctrlBind():
    objs = FBModelList()
    FBGetSelectedModels(objs, None, True, True)

    objCount = len(objs)
    if objCount>1:
        childBone = None
        chainBoneLst_Reverse = []

        # build bone chain and aim to child
        for i in range(objCount):
            sourceBone = objs[objCount-i-1]
            sourceBoneMatrix = FBMatrix()
            sourceBone.GetMatrix(sourceBoneMatrix)

            chainBone = FBModelSkeleton(sourceBone.Name+proxySubFix)
            chainBone.Show = True
            # chainBone.SetMatrix(sourceBoneMatrix)
            AlignTR( chainBone, sourceBone )
            chainBone.Size = sourceBone.Size*1.5

            # aim to child bone if possible
            if childBone:
                # chainBone.Scaling = FBVector3d(1,1,1)   # force normalize proxy bone scaling
                # print chainBone.Name
                # print chainBone.Scaling

                aimConstraint = creatConstraint('Aim')
                aimConstraint.ReferenceAdd(0,chainBone)
                aimConstraint.ReferenceAdd(1,childBone)
                aimConstraint.Active = True
                aimConstraint.PropertyList.Find("AimVector").Data = FBVector3d(1,0,0)
                aimConstraint.PropertyList.Find("WorldUpType").Data = 4 # assign to none

                FBSystem().Scene.Evaluate()

                aimConstraint.FBDelete()

                childBone.Parent = chainBone

            chainBoneLst_Reverse.append(chainBone)

            childBone = chainBone



        FBSystem().Scene.Evaluate()

        # set pre rotation
        for bone in chainBoneLst_Reverse:
            bone.PropertyList.Find("RotationActive").Data = True
            bone.PropertyList.Find("QuaternionInterpolate").Data = True
            bone.PropertyList.Find("PreRotation").Data = bone.PropertyList.Find("Lcl Rotation").Data
            bone.PropertyList.Find("Lcl Rotation").Data = bone.PropertyList.Find("PostRotation").Data

            # print chainBone.Rotation
        # fix end bone
        chainBoneLst_Reverse[0].PropertyList.Find("PreRotation").Data = chainBoneLst_Reverse[1].PropertyList.Find("PostRotation").Data
        # parent proxy chain to bone parent
        chainBoneLst_Reverse[-1].Parent = objs[0].Parent

        FBSystem().Scene.Evaluate()

        for i in range(objCount):
            sourceBone = objs[objCount-i-1]

            chainBone = chainBoneLst_Reverse[i]

            # constraint source to chain bone
            parentConstraint = creatConstraint('Parent/Child')
            parentConstraint.Name = sourceBone.Name+consSubFix
            parentConstraint.ReferenceAdd(0,sourceBone)
            parentConstraint.ReferenceAdd(1,chainBone)
            parentConstraint.Snap()
            parentConstraint.Lock = True

        for obj in objs:
            obj.Selected = False

        SelectBranch( chainBoneLst_Reverse[-1] )

    else:
        for obj in objs:
            obj.Selected = False

def ctrlBake():


    proxys = FBModelList()
    FBGetSelectedModels(proxys, None, True, True)

    for obj in proxys:
        obj.Selected = False
        if proxySubFix in obj.Name:
            baseName = obj.Name.replace(proxySubFix,"")
            baseBone = get_node(baseName)
            baseBone.Selected = True


    bakeAnim()
    # lPlotOptions = FBPlotOptions()
    # lPlotOptions.UseConstantKeyReducer = True
    # lPlotOptions.ConstantKeyReducerKeepOneKey = True
    # lPlotOptions.PlotAllTakes = False
    # lFrameRate = FBPlayerControl().GetTransportFps()
    # lPlotOptions.PlotPeriod = FBTime(0,0,0,1,0,lFrameRate)
    # FBSystem().CurrentTake.PlotTakeOnSelected( lPlotOptions )

    for obj in proxys:
        if proxySubFix in obj.Name:
            consName = obj.Name.replace(proxySubFix,"")+consSubFix
            a = FBComponentList()
            FBFindObjectsByName(consName, a, True, False )
            if a:
                parentConstraint = a[0]
                parentConstraint.FBDelete()

    for obj in proxys:
        if proxySubFix in obj.Name:
            obj.FBDelete()


def createCapsule(posA, posB, radius):
    # create a cylinder base on input sphere pos and radius
    # will cause too many extra issue if create a real capsule, like match up sphere and cylinder size and scale
    # so will just build a cylinder on vision side
    # but will still calculate collision as a capsule
    # to simplify minor stuff

    # create null to locate sphere
    nullA = FBModelNull('NullA'+capsuleSubFix)
    nullA.Translation = posA
    nullB = FBModelNull('NullB'+capsuleSubFix)
    nullB.Translation = posB

    cylinderLength = ((posB-posA).Length())/10/2
    cylinder = FBCreateObject( 'Browsing/Templates/Elements/Primitives', 'Cylinder', 'Cylinder')
    cylinder.Name = 'Cylinder'+capsuleSubFix
    cylinder.Scaling = FBVector3d(radius*2, cylinderLength, radius*2)
    cylinder.Translation = (posB-posA)*0.5+posA
    cylinder.Show = True

    # create constrain to place cylinder correctly
    posConstraint = creatConstraint('Position')
    posConstraint.ReferenceAdd(0,cylinder)
    posConstraint.ReferenceAdd(1,nullA)
    posConstraint.ReferenceAdd(1,nullB)
    posConstraint.Active = True

    aimConstraint = creatConstraint('Aim')
    aimConstraint.ReferenceAdd(0,cylinder)
    aimConstraint.ReferenceAdd(1,nullA)
    aimConstraint.Active = True
    aimConstraint.PropertyList.Find("AimVector").Data = FBVector3d(0,1,0)

    # delete constrains after use
    posConstraint.FBDelete()
    aimConstraint.FBDelete()

    nullA.Parent = cylinder
    nullB.Parent = cylinder
    
    # capsuleSet = FBSet('Set'+capsuleSubFix)
    # capsuleSet.ConnectSrc(cylinder)
    # capsuleSet.ConnectSrc(nullA)
    # capsuleSet.ConnectSrc(nullB)
    cShader = FBShaderManager().CreateShader("WireShader")
    cShader.Name = 'WireShader'+capsuleSubFix
    
    cylinder.ShadingMode = FBModelShadingMode.kFBModelShadingWire

    return cylinder



def addBody():
    radius = 1
    # create capsule for select obj
    objs = FBModelList()
    FBGetSelectedModels( objs )

    objs_B = []
    for obj in objs:
        if obj.Children: objs_B.append(obj)  # kick no children bone

    if objs_B:
        for obj in objs_B:
            pa = FBVector3d()
            obj.GetVector(pa)
            pb = FBVector3d()
            obj.Children[0].GetVector(pb)
            cylinder = createCapsule(pa, pb, radius)
            cylinder.Parent = obj
    else:
        # create capsule in ori point if nothing selected
        cylinder = createCapsule(FBVector3d(0, radius*30, 0), FBVector3d(0, -30*radius, 0), radius)

def deleteBody(isClear=False):
    if isClear:
        objs = FBComponentList()
        FBFindObjectsByName( '*'+capsuleSubFix+'*', objs, True, True )
    else:
        objs = FBModelList()
        FBGetSelectedModels( objs )

    for obj in objs:
        if capsuleSubFix in obj.Name:
            # delList.append(obj)
            for c in obj.Children:
                c.FBDelete()
            obj.FBDelete()

    # for obj in delList:
    #     obj.FBDelete()


def straightBone():
    # set local rotation of select bone as 0
    objs = FBModelList()
    FBGetSelectedModels( objs )

    if len(objs)>0:
        for obj in objs:
            v = FBVector3d()
            obj.SetVector(v, FBModelTransformationType.kModelRotation, False)

def copyBone():
    # print 'copy'
    # restore bone matrix
    global boneMatrixDict

    objs = FBModelList()
    FBGetSelectedModels( objs )

    if len(objs)>0:
        for obj in objs:
            # m = FBMatrix()
            # obj.GetMatrix(m)
            # boneMatrixDict[obj] = m
            # save local tranform only
            vt = FBVector3d()
            obj.GetVector(vt, FBModelTransformationType.kModelTranslation, False)
            vr = FBVector3d()
            obj.GetVector(vr, FBModelTransformationType.kModelRotation, False)
            boneMatrixDict[obj] = [vt,vr]

def pasteBone():

    # paste restored matrix if match
    objs = FBModelList()
    FBGetSelectedModels( objs )

    if len(objs)>0:
        for obj in objs:
            # print obj, boneMatrixDict[obj]
            if obj in boneMatrixDict.keys():
                vt = boneMatrixDict[obj][0]
                vr = boneMatrixDict[obj][1]
                # print vt, vr
                # apply local value
                obj.SetVector(vt, FBModelTransformationType.kModelTranslation, False)
                obj.SetVector(vr, FBModelTransformationType.kModelRotation, False)

def addWindCone():
    windCone = FBCreateObject( 'Browsing/Templates/Elements/Primitives', 'Cone', 'Cone')
    windCone.Name = windConeName
    windCone.Scaling = FBVector3d(1, 1, 1)
    windCone.Translation = FBVector3d(0, 0, 0)
    windCone.PropertyList.Find('GeometricTranslation').Data = FBVector3d(0, 10, 0)
    windCone.Show = True
    cShader = FBShaderManager().CreateShader("WireShader")
    cShader.Name = windConeName+'_WireShader'
    windCone.ShadingMode = FBModelShadingMode.kFBModelShadingWire

    windCone.PropertyCreate("MaxForce",FBPropertyType.kFBPT_float,"1.0",False,True,None)
    windCone.PropertyList.Find('MaxForce').Data = 1.0
    windCone.PropertyCreate("MinForce",FBPropertyType.kFBPT_float,"0.5",False,True,None)
    windCone.PropertyList.Find('MinForce').Data = 0.5
    windCone.PropertyCreate("Frequency",FBPropertyType.kFBPT_float,"1.0",False,True,None)
    windCone.PropertyList.Find('Frequency').Data = 1.0



def main():
    # prepare all information to call SpringMagicMB function

    # if os.environ['COMPUTERNAME'].lower() != base64.decodestring(compName):
    #     CreateWarning()
    #     return False

    springRatio = 1-float(spring_edit.Value)
    twistRatio = 1-float(twist_edit.Value)
    isLoop = bool(loop_button.State)
    isPoseMatch = bool(poseMatch_button.State)
    # get selection obj
    objs = FBModelList()
    FBGetSelectedModels(objs, None, True, True)

    # get frame range
    startFrame = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
    endFrame = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

    isFastMove = collision_fast_button.State
    isCollision = collision_button.State

    tension = tension_edit.Value

    extend=flex_edit.Value

    mass=mass_edit.Value

    if isCollision:
        subDiv = subDiv_edit.Value
    else:
        subDiv = 1.0


    # wind
    isWind=False
    windObj=None
    windMaxForce=windMinForce=windFreq=0
    modelList = FBComponentList()
    FBFindObjectsByName(windConeName, modelList, True, True )
    if modelList:
        windObj = modelList[0]

    if windObj:
        isWind = True
        windMaxForce = windObj.PropertyList.Find('MaxForce').Data
        windMinForce = windObj.PropertyList.Find('MinForce').Data
        windFreq = windObj.PropertyList.Find('Frequency').Data

    calStartTime = datetime.datetime.now()
    if len(objs)>0:
        SpringMagicMB(
                        objs,
                        springRatio,
                        twistRatio,
                        tension,
                        mass,
                        extend,
                        subDiv,
                        startFrame,
                        endFrame,
                        isLoop,
                        isPoseMatch,
                        isCollision,
                        isFastMove,
                        isWind,
                        windObj,
                        windMaxForce,
                        windMinForce,
                        windFreq
                    )
    calDeltaTime = (datetime.datetime.now() - calStartTime)
    print "Spring Calculation Time: {0}s".format(calDeltaTime.seconds)

def rotateObjByQuat(obj,quat):
    # rotate object by quatention value

    rotateMatrix = FBMatrix()
    obj.GetMatrix(rotateMatrix)
    # print rotateMatrix
    FBQuaternionToMatrix( rotateMatrix, quat)
    # FBQuaternionToMatrix( curObjMatrix, quat)

    # curObjMatrix *= rotateMatrix    # rotate obj matrix
    # print rotateMatrix
    obj.SetMatrix(rotateMatrix)
    return rotateMatrix


def get_node(name):
    a = FBComponentList()
    FBFindObjectsByName( name, a, True, True )
    if len(a)>0:
        return a[0]
    else:
        return None

def get_trans(n):
    v=FBVector3d()
    n.GetVector(v, FBModelTransformationType.kModelTranslation)
    return v
def get_rot(n, isWorld):
    v=FBVector3d()
    n.GetVector(v, FBModelTransformationType.kModelRotation, isWorld)
    return v
def get_matrix(n):
    m=FBMatrix()
    n.GetMatrix(m)
    return m

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def goto_frame(n):
    # check if n is a whole number of frame
    if int(n)-n==0:
        t = FBTime(0,0,0,int(n))
    else:
        lFrameRate = FBPlayerControl().GetTransportFpsValue()
        timeMilliSecond = 1000.0/lFrameRate*n
        t=FBTime()
        t.SetMilliSeconds(int(timeMilliSecond))

    # print t
    FBPlayerControl().Goto(t)

# collision part
def distance(a, b):
    return (b-a).Length()

def lerp_vec(a,b,t):
    return a*(1-t) + b*t

def dist_to_line(a,b,p):
    ap = p-a
    ab = b-a
    result = a + ab* (ap.DotProduct(ab)/ab.DotProduct(ab))
    return distance(result,p)

def dist_to_plane(q, n, d):
    return n.DotProduct(q) - d / n.DotProduct(n)

def is_same_side_of_plane(pt, test_pt, n, d):
    d1 = math.copysign(1, dist_to_plane(pt, n, d))
    d2 = math.copysign(1, dist_to_plane(test_pt, n, d))

    # print(pt, test_pt, d1,d2)
    return d1 * d2 == 1.0

def proj_pt_to_plane(pt, n, d):
    t = n.DotProduct(pt) - d
    return pt - n*t

def pt_in_sphere(pt, c, r):
    return (pt-c).Length() <= r

def pt_in_cylinder(pt, p, q, r):
    n = (q-p).Normalize()
    d = n.DotProduct(p)
    if not is_same_side_of_plane(pt, (p+q)/2.0, n, d):
        return False
    n = (q-p).Normalize()
    d = n.DotProduct(q)
    if not is_same_side_of_plane(pt, (p+q)/2.0, n, d):
        return False

    proj_pt = proj_pt_to_plane(pt, n, d)
    # print("proj_pt",proj_pt)
    # print("q",q)
    # print("distance(proj_pt,q)", distance(proj_pt,q))
    return distance(proj_pt,q) <= r

def test():
    global sa, sb, p, q
    sa = FBVector3d()
    get_node('bone_A').GetVector(sa)
    sb = FBVector3d()
    get_node('bone_B').GetVector(sb)

    p = FBVector3d()
    get_node('Sphere_A').GetVector(p)
    q = FBVector3d()
    get_node('Sphere_B').GetVector(q)

    r = 10

    print(pt_in_cylinder(sa, p, q, r))

#test()

def segment_sphere_isect(sa, sb, c, r):
    NotFound = (False, None)
    
    p = sa
    d = (sb-sa).Normalize()

    m = p - c
    b = m.DotProduct(d)
    c = m.DotProduct(m) - r * r

    if c > 0.0 and b > 0.0:
        return NotFound

    discr = b*b - c
    if discr < 0.0:
        return NotFound

    t = -b - math.sqrt(discr)
    if t < 0.0:
        return NotFound

    dist = distance(sa, sb)
    q = p + d * t
    return ((t>=0 and t<=dist), q)

EPSILON = 1e-6
def segment_cylinder_isect(sa, sb, p, q, r):
    d = q-p
    m = sa-p
    n = sb-sa
    md = m.DotProduct(d)
    nd = n.DotProduct(d)
    dd = d.DotProduct(d)

    NotFound = (False, None)
    if md < 0 and md + nd < 0:
        return NotFound

    if md > dd and md + nd > dd:
        return NotFound

    nn = n.DotProduct(n)
    mn = m.DotProduct(n)

    a = dd*nn - nd*nd
    k = m.DotProduct(m) - r*r
    c = dd*k - md*md

    if abs(a) < EPSILON:
        if c > 0:
            return NotFound
        if md < 0:
            t = -mn / nn
        elif md > dd:
            t = (nd - mn) / nn
        else:
            t = 0
        return (True, lerp_vec(sa, sb, t))

    b = dd*mn - nd*md
    discr = b*b - a*c
    if discr < 0:
        return NotFound

    t = (-b - math.sqrt(discr)) / a;
    if t < 0.0 or t > 1.0:
        return NotFound
    if (md + t * nd < 0.0):
        if nd <= 0.0:
            return NotFound
        t = -md / nd;
        return (k + 2 * t * (mn + t * nn) <= 0.0,
                lerp_vec(sa, sb, t))
    elif md + t * nd > dd:
        if nd >= 0.0:
            return NotFound
        t = (dd - md) / nd;
        return (k + dd - 2 * md + t * (2 * (mn - nd) + t * nn) <= 0.0,
                lerp_vec(sa, sb, t))

    return (True, lerp_vec(sa, sb, t))

# test = segment_cylinder_isect(FBVector3d(-2,0.5, 0), FBVector3d(2,0.5, 0), FBVector3d(0,0,0), FBVector3d(0,0.25,0), 1)
# print(test)

def pt_in_capsule(pt, p, q, r):
    return pt_in_cylinder(pt, p, q, r) or pt_in_sphere(pt, p, r) or pt_in_sphere(pt, q, r)
    
def segment_capsule_isect(sa, sb, p, q, r):
    # sa = FBVector3d()
    #    ray start point pos vector
    # sb = FBVector3d()
    #    ray end point pos vector
    # p = FBVector3d()
    #    capsle one sphere tip pos
    # q = FBVector3d()
    #    capsle another sphere tip pos
    # r = float
    #    radio of capsle sphere

    if pt_in_capsule(sa, p, q, r) and pt_in_capsule(sb, p, q, r):
        # both inside.  extend sb to get intersection
        newb = sa + (sb-sa).Normalize() * 200.0
        sa, sb = newb, sa
    elif pt_in_capsule(sa, p, q, r):
        sb, sa = sa, sb
    
    d = (sb-sa).Normalize()

    i1 = segment_sphere_isect(sa, sb, p, r)
    i2 = segment_sphere_isect(sa, sb, q, r)
    i3 = segment_cylinder_isect(sa, sb, p, q, r)

    dist = float('inf')
    closest_pt = None
    hit = False
    hitCylinder = False
    if i1[0]:
        hit = True
        pt = i1[1]
        if distance(sa, pt) < dist:
            closest_pt = pt
        dist = min(dist, distance(sa, pt))
        # draw_locator(i1[2], 'i1')
    if i2[0]:
        hit = True
        pt = i2[1]
        if distance(sa, pt) < dist:
            closest_pt = pt
        dist = min(dist, distance(sa, pt))
    if i3[0]:
        hit = True
        hitCylinder = True
        pt = i3[1]
        if distance(sa, pt) < dist:
            closest_pt = pt
        dist = min(dist, distance(sa, pt))

    return (hit, closest_pt, hitCylinder)



# kartick functions end

def drawDebug_box(pos):
    null = FBModelCube('col')
    null.SetVector(pos)
    null.Show = True

def preCheckCollision(objPos,objLength,capsuleLst):
    # pre check bone length compare with collision body radius
    # print obj.Name+'_col_'+str(i)
    for obj in capsuleLst:
        # print obj.Name
        p = FBVector3d()
        obj.Children[0].GetVector(p)
        q = FBVector3d()
        obj.Children[1].GetVector(q)
        r = obj.Scaling[0]*10/2
        boneToCapsuleDistance = dist_to_line(p,q,objPos)
        if boneToCapsuleDistance<objLength+r:  # means close enough to have a hit change
            return True

    return False


def checkCollision(cur_pos, pre_pos, capsuleLst, isReverse):
    # calculate collision with all the capsule in scene

    if not isReverse:
        sa = cur_pos
        sb = pre_pos
    else:
        sb = cur_pos
        sa = pre_pos        

    isHited = False
    closest_pt_dict = {}
    for obj in capsuleLst:
        p = FBVector3d()
        obj.Children[0].GetVector(p)
        q = FBVector3d()
        obj.Children[1].GetVector(q)
        # r = obj.Scaling[0]/2
        r = obj.Scaling[0]*10/2

        hit, closest_pt, hitCylinder = segment_capsule_isect(sa, sb, p, q, r)

        if hit:
            isHited = True
            closest_pt_dict[obj.Name] = [obj,closest_pt]
            # drawDebug_box(closest_pt)

    if isHited:
        pt_length = 9999
        closest_pt = None
        col_obj = None
        for pt in closest_pt_dict.keys():
            lLength = (closest_pt_dict[pt][1]-pre_pos).Length()
            if lLength < pt_length:
                pt_length = lLength
                closest_pt = closest_pt_dict[pt][1]
                col_obj = closest_pt_dict[pt][0]

        # drawDebug_box(closest_pt)
        # for null in col_obj.Children:
        #     if 'NullB' in null.Name:
        #         pass
        # return col pt and col_body speed
        return closest_pt, col_obj, hitCylinder
    else:
        return None, None, None

def keyCandidate(obj, isTranslation, isRotation):
    # use FBPlayerControl().Key() to set key is about 20% slower than keyCandidate
    if isTranslation:
        if obj.Translation.GetAnimationNode():
            obj.Translation.GetAnimationNode().KeyCandidate()
    if isRotation:
        if obj.Rotation.GetAnimationNode():
            obj.Rotation.GetAnimationNode().KeyCandidate()

def aim_by_ratio(obj,prePos,curPos,ratio,upVector,preGrandPos=None,tension=0):
    aimConstraint = creatConstraint('Aim')

    aimConstraint.ReferenceAdd(0,obj)
    
    preNull = FBModelNull('preNull')
    preNull.SetVector(prePos)
    aimConstraint.ReferenceAdd(1,preNull)

    curNull = FBModelNull('curNull')
    curNull.SetVector(curPos)
    aimConstraint.ReferenceAdd(1,curNull)

    aimConstraint.PropertyList.Find("AimVector").Data = FBVector3d(1,0,0)
    aimConstraint.PropertyList.Find("UpVector").Data = FBVector3d(0,1,0)
    aimConstraint.PropertyList.Find("WorldUpType").Data = 3 # assign to vector
    aimConstraint.PropertyList.Find("WorldUpVector").Data = upVector

    aimConstraint.PropertyList.Find(preNull.Name+".Weight").Data = 1-ratio
    aimConstraint.PropertyList.Find(curNull.Name+".Weight").Data = ratio
    # print preGrandPos
    if preGrandPos:
        preGrandNull = FBModelNull('preGrandNull')
        preGrandNull.SetVector(preGrandPos)
        aimConstraint.ReferenceAdd(1,preGrandNull)

        aimConstraint.PropertyList.Find(preGrandNull.Name+".Weight").Data = (1-ratio)*tension

    aimConstraint.Active = True

    FBSystem().Scene.Evaluate()

    keyCandidate(obj,False,True)


    aimConstraint.FBDelete()
    # aimConstraint.Active = False
    preNull.FBDelete()
    curNull.FBDelete()

    if preGrandPos:
        preGrandNull.FBDelete()

def get_col_body():
    a = FBComponentList()
    FBFindObjectsByName( 'Cylinder'+capsuleSubFix+'*', a, True, True )
    return a

def get_col_body_pos():
    col_body_pos_dict = {}
    # FBPlayerControl().SnapMode = FBTransportSnapMode.kFBTransportSnapModeNoSnap
    col_body_list = get_col_body()
    for body in col_body_list:
        for null in body.Children:
            if 'NullB' in null.Name:
                v = FBVector3d()
                null.GetVector(v)
                col_body_pos_dict[body] = v
    return col_body_pos_dict

def getMatrixRow(matrix, row):
    rowLst = []
    rowLst.append(matrix[row*4+0])
    rowLst.append(matrix[row*4+1])
    rowLst.append(matrix[row*4+2])
    return rowLst

def offsetPosByDirection(sDirection,tPos,moveDistance):
    # get new target pos
    tPos += sDirection.Normalize()*moveDistance

    return tPos

def SpringMagicMB(
                    objs,
                    ratio=0.3,
                    twistRatio=0.3,
                    tension=0.5,
                    mass=0.0,
                    extend=0.0,
                    subDiv=1.0,
                    startFrame=0,
                    endFrame=1,
                    isLoop=False,
                    isPoseMatch=True,
                    isCollision=False,
                    isFastMove=False,
                    isWind=False,
                    windObj=None,
                    windMaxForce=0,
                    windMinForce=0,
                    windFreq=0
                ):
    # on each frame go through all objs and do:
    # 1. make a vectorA from current obj position to previouse child position
    # 2. make a vectorB from current obj position to current child position
    # 3. calculate the angle between two vectors
    # 4. rotate the obj towards vectorA base on spring value

    # key point: rotate a matrix alone a surface by angle

    ratio /= subDiv
    twistRatio /= subDiv
    tension /= 1/(sigmoid(1-subDiv)+0.5)
    # import math
    # initial var
    preObjMatrix = FBMatrix()
    curObjMatrix = FBMatrix()

    preVector = FBVector3d()
    curVector = FBVector3d()
    preObjPos = FBVector3d()
    curObjPos = FBVector3d()
    preChildPos = FBVector3d()
    curChildPos = FBVector3d()
    rotateAxis = FBVector3d()
    preRotateAxis = FBVector3d()
    rotateDegree = 0.0

    startTime = FBTime(0, 0, 0, startFrame)
    endTime = FBTime(0, 0, 0, endFrame)
    isSeconendPath = False

    # loop frame
    obj_trans_dict = {} # use a dict to restore obj previous frame trans information
    i = 0.0
    FBPlayerControl().SnapMode = FBTransportSnapMode.kFBTransportSnapModeNoSnap

    capsuleLst = FBComponentList()
    FBFindObjectsByName( 'Cylinder'+capsuleSubFix+'*', capsuleLst, True, True )

    # Create a FBProgress object and set default values for the caption and text.
    lFbp = FBProgress()

    # Call ProgressBegin() before use any other function and property.
    lFbp.ProgressBegin()

    # Set the custom task name.
    lFbp.Caption = "Spring Magic"

    while i < ((endFrame-startFrame)+1/subDiv):

        # Stop the progress if user request cancellation by pressing and holding "ESC" key
        if (lFbp.UserRequestCancell()):
            break

        if isSeconendPath:
            lFbp.Text = "Loop Path ..."
        else:
            lFbp.Text = "First Path ..."

        pVal = int(i/(endFrame-startFrame+1)*100)
        lFbp.Percent = pVal

        # print 'Frame',i

        goto_frame(startFrame+i)
        FBSystem().Scene.Evaluate()  # update scene
        # print str(FBSystem().LocalTime.GetMilliSeconds())

        # calculate obj
        for obj in objs:
            if len(obj.Children)>0 and (obj.Parent is not None):     # skip end bone and root bone
                child = obj.Children[0]
                # grand child for tension
                grandChild = None
                if obj.Children[0].Children:
                    grandChild = child.Children[0]
                if i > 0 or isSeconendPath:     # only skip first frame of first calculation path

                    prev_obj_pos = obj_trans_dict[obj][0]
                    prev_child_pos = obj_trans_dict[obj][1]
                    prevprev_child_pos = obj_trans_dict[obj][7]
                    bonePreDis = obj_trans_dict[obj][8]
                    prev_grandChild_pos = obj_trans_dict[obj][3]
                    hasChildCollide = obj_trans_dict[obj][4]
                    boneLength = obj_trans_dict[obj][5]
                    # print prev_obj_pos
                    # print prev_child_pos

                    # get prev_rot for twist
                    prev_rot = obj_trans_dict[obj][2]

                    # get current frame position of obj and child
                    cur_obj_pos = get_trans(obj)
                    # print obj.Name+nullSubFix
                    objNull = get_node(obj.Name+nullSubFix)
                    cur_child_pos = get_trans(objNull)
                    # cur_child_pos = get_trans(child)
                    if mass > 0.0:
                        smBoneRefLocOffsetDir = cur_child_pos - prev_child_pos
                        smBoneRefLocOffsetDistance = distance(cur_child_pos,prev_child_pos)*(1-ratio)*(1-mass)
                        cur_child_pos = offsetPosByDirection(smBoneRefLocOffsetDir,cur_child_pos,(smBoneRefLocOffsetDistance/subDiv))
                    # get cur_rot for twist
                    cur_rot = FBVector3d()
                    objNull.GetVector(cur_rot, FBModelTransformationType.kModelRotation)

                    # apply mass
                    forceDir = prev_child_pos - prevprev_child_pos
                    forceDistance = bonePreDis*mass
                    cur_child_pos = offsetPosByDirection(forceDir,cur_child_pos,(forceDistance/subDiv))

                    # apply wind
                    if isWind:
                        windMaxForce = windObj.PropertyList.Find('MaxForce').Data
                        windMinForce = windObj.PropertyList.Find('MinForce').Data
                        windFreq = windObj.PropertyList.Find('Frequency').Data

                        midForce = (windMaxForce+windMinForce)/2

                        # get source x-axis direction in world space
                        windDirection = getMatrixRow(get_matrix(windObj),1)
                        # sDirection = sObj.getMatrix()[0][:3]
                        windDirection = FBVector3d(windDirection[0],windDirection[1],windDirection[2]).Normalize()
                        windDistance = math.sin(i*windFreq)*(windMaxForce-windMinForce)+midForce

                        cur_child_pos = offsetPosByDirection(windDirection,cur_child_pos,windDistance)

                        # print prev_child_pos

                    col_pre = col_cur = None
                    # detect collision
                    if isCollision and capsuleLst:
                        # check col from previous pos to cur pos

                        # for kkk in capsuleLst:
                        #     print kkk.Name
                        if preCheckCollision(cur_obj_pos,boneLength,capsuleLst):

                            col_pre, col_body_pre, hitCylinder_pre = checkCollision(cur_child_pos, prev_child_pos, capsuleLst, True)

                            col_cur, col_body_cur, hitCylinder_cur = checkCollision(cur_child_pos, prev_child_pos, capsuleLst, False)

                            if col_pre and (col_cur == None):
                                cur_child_pos = col_pre
                                # cur_child_pos += (col_pre-cur_child_pos)*threshold_rate
                                # ratio = 1   # move to

                            elif col_cur and (col_pre == None):
                                prev_child_pos = col_cur
                                # prev_child_pos += (col_cur-prev_child_pos)*threshold_rate
                                # ratio = 0
                            elif col_pre and col_cur:

                                midPoint = (prev_child_pos+cur_child_pos)/2
                                if distance(col_pre, midPoint) < distance(col_cur, midPoint):
                                    cur_child_pos = col_pre
                                    if isFastMove:
                                        prev_child_pos = col_pre

                                else:
                                    cur_child_pos = col_cur
                                    if isFastMove:
                                        prev_child_pos = col_cur

                    # calculate upvector by interpolation y axis for twist
                    prev_obj_yAxis = obj_trans_dict[obj][6]

                    cur_obj_yAxis = getMatrixRow(get_matrix(objNull),1)

                    prev_upVector = FBVector3d(prev_obj_yAxis[0],prev_obj_yAxis[1],prev_obj_yAxis[2]).Normalize()
                    cur_upVector = FBVector3d(cur_obj_yAxis[0],cur_obj_yAxis[1],cur_obj_yAxis[2]).Normalize()

                    upVector = prev_upVector*(1-twistRatio)+cur_upVector*(twistRatio)

                    # apply aim constraint
                    if tension>0 and prev_grandChild_pos and hasChildCollide:
                        aim_by_ratio(obj, prev_child_pos, cur_child_pos, ratio, upVector, prev_grandChild_pos, tension)
                    else:
                        aim_by_ratio(obj, prev_child_pos, cur_child_pos, ratio, upVector)

                    #apply twist on x axis
                    # r = FBVector3d()
                    upVector = getMatrixRow(get_matrix(obj),1)

                    if extend != 0.0 and child:
                        childT = child.Translation
                        # get length between bone pos and previous child pos
                        x2 = distance(prev_child_pos,get_trans(obj))
                        x3 = boneLength*(1-extend) + x2*extend
                        child.Translation = FBVector3d([x3,childT[1],childT[2]])
                        FBSystem().Scene.Evaluate()
                        keyCandidate(child,True,False)

                    FBSystem().Scene.Evaluate() #update scene
                    # set key
                    keyCandidate(obj,True,True)

                    # restore for next frame
                    cur_obj_pos = get_trans(obj)
                    cur_child_pos = get_trans(child)
                    cur_grandChild_pos = False
                    # print grandChild.Name
                    if prev_grandChild_pos:
                        cur_grandChild_pos = get_trans(grandChild)
                    # change parent obj hasChildCollide value
                    if col_pre or col_cur:
                        hasChildCollide = True
                    else:
                        hasChildCollide = False
                    if obj.Parent in obj_trans_dict.keys():
                        obj_trans_dict[obj.Parent][4] = hasChildCollide
                    bonePreDis = distance(prev_child_pos,prevprev_child_pos)
                    obj_trans_dict[obj] = [cur_obj_pos,cur_child_pos,0,cur_grandChild_pos,hasChildCollide,boneLength,upVector,prev_child_pos,bonePreDis]

                else:
                    # creat a null at child pos, then parent to obj parent for calculation
                    null = FBModelNull(obj.Name+nullSubFix)

                    if isPoseMatch:
                        ttt = 0.0
                        null.Parent = obj.Parent

                        null.Rotation.SetAnimated(True)
                        null.Translation.SetAnimated(True)

                        while ttt < (endFrame-startFrame):
                            goto_frame(startFrame+ttt)
                            FBSystem().Scene.Evaluate()  # update scene

                            childMatrix = FBMatrix()
                            child.GetMatrix(childMatrix)
                            null.SetMatrix(childMatrix)

                            keyCandidate(null,True,True)

                            ttt += 1.0
                        goto_frame(startFrame)

                    else:
                        null.Parent = obj.Parent
                        childMatrix = FBMatrix()
                        child.GetMatrix(childMatrix)
                        null.SetMatrix(childMatrix)


                        # if not obj.Rotation.IsAnimated:
                        obj.Rotation.SetAnimated(True)
                        
                        # will cause error if use for loop to process this
                        if obj.Rotation.GetAnimationNode():
                            obj.Rotation.GetAnimationNode().Nodes[0].FCurve.KeyDeleteByTimeRange(startTime, endTime, False)
                            obj.Rotation.GetAnimationNode().Nodes[1].FCurve.KeyDeleteByTimeRange(startTime, endTime, False)
                            obj.Rotation.GetAnimationNode().Nodes[2].FCurve.KeyDeleteByTimeRange(startTime, endTime, False)


                        obj.Translation.SetAnimated(True)

                        if obj.Translation.GetAnimationNode():
                            obj.Translation.GetAnimationNode().Nodes[0].FCurve.KeyDeleteByTimeRange(startTime, endTime, False)
                            obj.Translation.GetAnimationNode().Nodes[1].FCurve.KeyDeleteByTimeRange(startTime, endTime, False)
                            obj.Translation.GetAnimationNode().Nodes[2].FCurve.KeyDeleteByTimeRange(startTime, endTime, False)

                        FBSystem().Scene.Evaluate() #update scene
                        # set key
                        keyCandidate(obj,True,True)

                    # get initial position of obj and child
                    prev_obj_pos = get_trans(obj)
                    # print get_matrix(obj)[4:7]
                    prev_obj_yAxis = getMatrixRow(get_matrix(obj),1)
                    prev_child_pos = get_trans(child)
                    boneLength = distance(prev_obj_pos,prev_child_pos)
                    prev_grandChild_pos = False

                    if grandChild:
                        prev_grandChild_pos = get_trans(grandChild)

                    # get prev_rot for twist
                    prev_rot = FBVector3d()
                    obj.GetVector(prev_rot, FBModelTransformationType.kModelRotation)

                    # restore obj trans information
                    obj_trans_dict[obj] = [prev_obj_pos,prev_child_pos,prev_rot,prev_grandChild_pos,False,boneLength,prev_obj_yAxis,prev_child_pos,0.0]

                    # # get collision
                    # if collision_button.State:
                    #     col_body_pos_dict = get_col_body_pos()

        i += 1/subDiv

        # print isLoop, startFrame+i+1, endFrame
        if isLoop and (startFrame+i > endFrame) and isSeconendPath == False: # at the end frame of first path
            i = 0   # back to first frame
            isSeconendPath = True   # mark seconed path calculation for loop


    # bake result
    bakeAnim()

    # remove all spring nulls
    a = FBComponentList()
    FBFindObjectsByName( '*'+nullSubFix+'*', a, True, True )
    for null in a:
        null.FBDelete()

    FBPlayerControl().SnapMode = FBTransportSnapMode.kFBTransportSnapModeSnapOnFrames
    lFbp.Percent = 100
    lFbp.ProgressDone()

    # print curVector

def bakeAnim():
    lPlotOptions = FBPlotOptions()
    lPlotOptions.UseConstantKeyReducer = True
    lPlotOptions.ConstantKeyReducerKeepOneKey = True
    lPlotOptions.PlotAllTakes = False
    lFrameRate = FBPlayerControl().GetTransportFps()
    lPlotOptions.PlotPeriod = FBTime(0,0,0,1,0,lFrameRate)
    FBSystem().CurrentTake.PlotTakeOnSelected( lPlotOptions.PlotPeriod )

def PopulateTool(t):
    #populate regions here

    x = FBAddRegionParam(8,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(45,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("spring_lable","spring_lable", x, y, w, h)

    t.SetControl("spring_lable", spring_lable)
    spring_lable.Visible = True
    spring_lable.ReadOnly = True
    spring_lable.Enabled = True
    spring_lable.Hint = ""
    spring_lable.Caption = "Spring:"
    spring_lable.Style = FBTextStyle.kFBTextStyleNone
    spring_lable.Justify = FBTextJustify.kFBTextJustifyCenter
    spring_lable.WordWrap = False
    
    x = FBAddRegionParam(50,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("spring_edit","spring_edit", x, y, w, h)

    t.SetControl("spring_edit", spring_edit)
    spring_edit.Visible = True
    spring_edit.ReadOnly = False
    spring_edit.Enabled = True
    spring_edit.Hint = "0 to 1, the bigger the softer result"
    spring_edit.Value = 0.7
    spring_edit.Min = 0.0
    spring_edit.Max = 1.0
    
    x = FBAddRegionParam(85,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(40,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("twist_lable","twist_lable", x, y, w, h)

    t.SetControl("twist_lable", twist_lable)
    twist_lable.Visible = True
    twist_lable.ReadOnly = True
    twist_lable.Enabled = True
    twist_lable.Hint = ""
    twist_lable.Caption = "Twist:"
    twist_lable.Style = FBTextStyle.kFBTextStyleNone
    twist_lable.Justify = FBTextJustify.kFBTextJustifyRight
    twist_lable.WordWrap = False
    
    x = FBAddRegionParam(125,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("twist_edit","twist_edit", x, y, w, h)

    t.SetControl("twist_edit", twist_edit)
    twist_edit.Visible = True
    twist_edit.ReadOnly = False
    twist_edit.Enabled = True
    twist_edit.Hint = "0 to 1, the bigger the softer result, affect X axis"
    twist_edit.Value = 0.7
    twist_edit.Min = 0.0
    twist_edit.Max = 1.0

    x = FBAddRegionParam(235,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(50,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("tension_lable","tension_lable", x, y, w, h)

    t.SetControl("tension_lable", tension_lable)
    tension_lable.Visible = False
    tension_lable.ReadOnly = True
    tension_lable.Enabled = True
    tension_lable.Hint = ""
    tension_lable.Caption = "Tension:"
    tension_lable.Style = FBTextStyle.kFBTextStyleNone
    tension_lable.Justify = FBTextJustify.kFBTextJustifyRight
    tension_lable.WordWrap = False
    
    x = FBAddRegionParam(280,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("tension_edit","tension_edit", x, y, w, h)

    t.SetControl("tension_edit", tension_edit)
    tension_edit.Visible = False
    tension_edit.ReadOnly = False
    tension_edit.Enabled = True
    tension_edit.Hint = "0 to 1, the connection tension between chain node, can reduce the poping of collision"
    tension_edit.Value = 0.5
    tension_edit.Min = 0.0
    tension_edit.Max = 1.0

    x = FBAddRegionParam(235,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(50,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("mass_lable","mass_lable", x, y, w, h)

    t.SetControl("mass_lable", mass_lable)
    mass_lable.Visible = True
    mass_lable.ReadOnly = True
    mass_lable.Enabled = True
    mass_lable.Hint = ""
    mass_lable.Caption = "Inertia:"
    mass_lable.Style = FBTextStyle.kFBTextStyleNone
    mass_lable.Justify = FBTextJustify.kFBTextJustifyRight
    mass_lable.WordWrap = False

    x = FBAddRegionParam(282,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("mass_edit","mass_edit", x, y, w, h)

    t.SetControl("mass_edit", mass_edit)
    mass_edit.Visible = True
    mass_edit.ReadOnly = False
    mass_edit.Enabled = True
    mass_edit.Hint = "0 to 1, the inertia value of the chain, to show weight result"
    mass_edit.Value = 0.0
    mass_edit.Min = 0.0
    mass_edit.Max = 1.0


    x = FBAddRegionParam(160,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("flex_lable","flex_lable", x, y, w, h)

    t.SetControl("flex_lable", flex_lable)
    flex_lable.Visible = True
    flex_lable.ReadOnly = True
    flex_lable.Enabled = True
    flex_lable.Hint = ""
    flex_lable.Caption = "Flex:"
    flex_lable.Style = FBTextStyle.kFBTextStyleNone
    flex_lable.Justify = FBTextJustify.kFBTextJustifyRight
    flex_lable.WordWrap = False
    
    x = FBAddRegionParam(195,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("flex_edit","flex_edit", x, y, w, h)

    t.SetControl("flex_edit", flex_edit)
    flex_edit.Visible = True
    flex_edit.ReadOnly = False
    flex_edit.Enabled = True
    flex_edit.Hint = "0 to 1, flexibility of the chain, squash and stratch effect"
    flex_edit.Value = 0.0
    flex_edit.Min = 0.0
    flex_edit.Max = 1.0

    x = FBAddRegionParam(45,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(60,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(65,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("subDiv_lable","subDiv_lable", x, y, w, h)

    t.SetControl("subDiv_lable", subDiv_lable)
    subDiv_lable.Visible = True
    subDiv_lable.ReadOnly = True
    subDiv_lable.Enabled = True
    subDiv_lable.Hint = ""
    subDiv_lable.Caption = "Sub-Key:"
    subDiv_lable.Style = FBTextStyle.kFBTextStyleNone
    subDiv_lable.Justify = FBTextJustify.kFBTextJustifyRight
    subDiv_lable.WordWrap = False

    x = FBAddRegionParam(110,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(60,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(40,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("subDiv_edit","subDiv_edit", x, y, w, h)

    t.SetControl("subDiv_edit", subDiv_edit)
    subDiv_edit.Visible = True
    subDiv_edit.ReadOnly = False
    subDiv_edit.Enabled = True
    subDiv_edit.Hint = "Default value is 1, if set as 5, means will step as 1/5 frame to calculation"
    subDiv_edit.Value = 1
    subDiv_edit.Min = 0
    subDiv_edit.Max = 100
    
    x = FBAddRegionParam(260,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(60,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(50,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("loop_button","loop_button", x, y, w, h)

    t.SetControl("loop_button", loop_button)
    loop_button.Visible = True
    loop_button.ReadOnly = False
    loop_button.Enabled = True
    loop_button.Hint = "Do 2 times calculation to get loop result"
    loop_button.Caption = "Loop"
    loop_button.State = 0
    loop_button.Style = FBButtonStyle.kFBCheckbox
    loop_button.Justify = FBTextJustify.kFBTextJustifyLeft
    loop_button.Look = FBButtonLook.kFBLookNormal

    x = FBAddRegionParam(165,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(60,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(90,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("poseMatch_button","poseMatch_button", x, y, w, h)

    t.SetControl("poseMatch_button", poseMatch_button)
    poseMatch_button.Visible = True
    poseMatch_button.ReadOnly = False
    poseMatch_button.Enabled = True
    poseMatch_button.Hint = "Make result close to exists keyframe pose"
    poseMatch_button.Caption = "Pose Match"
    poseMatch_button.State = 1
    poseMatch_button.Style = FBButtonStyle.kFBCheckbox
    poseMatch_button.Justify = FBTextJustify.kFBTextJustifyLeft
    poseMatch_button.Look = FBButtonLook.kFBLookNormal
    
    x = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(40,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("range_lable","range_lable", x, y, w, h)

    t.SetControl("range_lable", range_lable)
    range_lable.Visible = True
    range_lable.ReadOnly = True
    range_lable.Enabled = True
    range_lable.Hint = ""
    range_lable.Caption = "Range:"
    range_lable.Style = FBTextStyle.kFBTextStyleNone
    range_lable.Justify = FBTextJustify.kFBTextJustifyLeft
    range_lable.WordWrap = True
    
    x = FBAddRegionParam(65,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(40,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(65,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("range_button","range_button", x, y, w, h)

    t.SetControl("range_button", range_button)
    range_button.Visible = True
    range_button.ReadOnly = True
    range_button.Enabled = True
    range_button.Hint = "Current time line range"
    range_button.Caption = "Active"
    range_button.State = 1
    range_button.Style = FBButtonStyle.kFBCheckbox
    range_button.Justify = FBTextJustify.kFBTextJustifyLeft
    range_button.Look = FBButtonLook.kFBLookNormal

    x = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(90,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(90,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("collision_button","collision_button", x, y, w, h)

    t.SetControl("collision_button", collision_button)
    collision_button.Visible = True
    collision_button.ReadOnly = False
    collision_button.Enabled = True
    collision_button.Hint = "Is active collision calculation, will take more time"
    collision_button.Caption = "Collision:"
    collision_button.State = 0
    collision_button.Style = FBButtonStyle.kFBCheckbox
    collision_button.Justify = FBTextJustify.kFBTextJustifyLeft
    collision_button.Look = FBButtonLook.kFBLookNormal

    x = FBAddRegionParam(230,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(90,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(90,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("collision_fast_button","collision_fast_button", x, y, w, h)

    t.SetControl("collision_fast_button", collision_fast_button)
    collision_fast_button.Visible = True
    collision_fast_button.ReadOnly = False
    collision_fast_button.Enabled = True
    collision_fast_button.Hint = "Is collide with fast move object"
    collision_fast_button.Caption = "Fast Move"
    collision_fast_button.State = 0
    collision_fast_button.Style = FBButtonStyle.kFBCheckbox
    collision_fast_button.Justify = FBTextJustify.kFBTextJustifyLeft
    collision_fast_button.Look = FBButtonLook.kFBLookNormal

    x = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(125,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("bone_lable","bone_lable", x, y, w, h)

    t.SetControl("bone_lable", bone_lable)
    bone_lable.Visible = True
    bone_lable.ReadOnly = True
    bone_lable.Enabled = True
    bone_lable.Hint = ""
    bone_lable.Caption = 'Bone:'
    bone_lable.Style = FBTextStyle.kFBTextStyleNone
    bone_lable.Justify = FBTextJustify.kFBTextJustifyRight
    bone_lable.WordWrap = False

    # x = FBAddRegionParam(5,FBAttachType.kFBAttachNone,"")
    # y = FBAddRegionParam(70,FBAttachType.kFBAttachNone,"")
    # w = FBAddRegionParam(35,FBAttachType.kFBAttachNone,"")
    # h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    # t.AddRegion("local_lable","local_lable", x, y, w, h)

    # t.SetControl("local_lable", local_lable)
    # local_lable.Visible = True
    # local_lable.ReadOnly = True
    # local_lable.Enabled = True
    # local_lable.Hint = ""
    # local_lable.Caption = 'Local'
    # local_lable.Style = FBTextStyle.kFBTextStyleNone
    # local_lable.Justify = FBTextJustify.kFBTextJustifyRight
    # local_lable.WordWrap = False
    
    x = FBAddRegionParam(60,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(120,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(70,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("straightBone_button","straightBone_button", x, y, w, h)

    t.SetControl("straightBone_button", straightBone_button)
    straightBone_button.Visible = True
    straightBone_button.ReadOnly = False
    straightBone_button.Enabled = True
    straightBone_button.Hint = "Set bone rotation to 0"
    straightBone_button.Caption = "Straight"
    straightBone_button.State = 0
    straightBone_button.Style = FBButtonStyle.kFBPushButton
    straightBone_button.Justify = FBTextJustify.kFBTextJustifyCenter
    straightBone_button.Look = FBButtonLook.kFBLookNormal
    straightBone_button.OnClick.Add(BtnCallbackstraightBone_button)

    x = FBAddRegionParam(140,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(120,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(45,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("copyBone_button","copyBone_button", x, y, w, h)

    t.SetControl("copyBone_button", copyBone_button)
    copyBone_button.Visible = True
    copyBone_button.ReadOnly = False
    copyBone_button.Enabled = True
    copyBone_button.Hint = "Copy bone pose"
    copyBone_button.Caption = "Copy"
    copyBone_button.State = 0
    copyBone_button.Style = FBButtonStyle.kFBPushButton
    copyBone_button.Justify = FBTextJustify.kFBTextJustifyCenter
    copyBone_button.Look = FBButtonLook.kFBLookNormal
    copyBone_button.OnClick.Add(BtnCallbackcopyBone_button)

    x = FBAddRegionParam(190,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(120,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(50,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("pasteBone_button","pasteBone_button", x, y, w, h)

    t.SetControl("pasteBone_button", pasteBone_button)
    pasteBone_button.Visible = True
    pasteBone_button.ReadOnly = False
    pasteBone_button.Enabled = True
    pasteBone_button.Hint = "Paste bone pose"
    pasteBone_button.Caption = "Paste"
    pasteBone_button.State = 0
    pasteBone_button.Style = FBButtonStyle.kFBPushButton
    pasteBone_button.Justify = FBTextJustify.kFBTextJustifyCenter
    pasteBone_button.Look = FBButtonLook.kFBLookNormal
    pasteBone_button.OnClick.Add(BtnCallbackpasteBone_button)

    x = FBAddRegionParam(190,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(155,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(100,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("branch_button","branch_button", x, y, w, h)

    t.SetControl("branch_button", branch_button)
    branch_button.Visible = True
    branch_button.ReadOnly = False
    branch_button.Enabled = True
    branch_button.Hint = "Select all children of current object"
    branch_button.Caption = "Select Branch"
    branch_button.State = 0
    branch_button.Style = FBButtonStyle.kFBPushButton
    branch_button.Justify = FBTextJustify.kFBTextJustifyCenter
    branch_button.Look = FBButtonLook.kFBLookNormal
    branch_button.OnClick.Add(BtnCallbackbranch_button)

    x = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(160,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(70,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("ctrl_lable","ctrl_lable", x, y, w, h)

    t.SetControl("ctrl_lable", ctrl_lable)
    ctrl_lable.Visible = True
    ctrl_lable.ReadOnly = True
    ctrl_lable.Enabled = True
    ctrl_lable.Hint = ""
    ctrl_lable.Caption = 'Controller:'
    ctrl_lable.Style = FBTextStyle.kFBTextStyleNone
    ctrl_lable.Justify = FBTextJustify.kFBTextJustifyRight
    ctrl_lable.WordWrap = False

    x = FBAddRegionParam(85,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(155,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(45,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("ctrlBind_button","ctrlBind_button", x, y, w, h)

    t.SetControl("ctrlBind_button", ctrlBind_button)
    ctrlBind_button.Visible = True
    ctrlBind_button.ReadOnly = False
    ctrlBind_button.Enabled = True
    ctrlBind_button.Hint = "Bind Bone Chain To Selected Controllers"
    ctrlBind_button.Caption = "Bind"
    ctrlBind_button.State = 0
    ctrlBind_button.Style = FBButtonStyle.kFBPushButton
    ctrlBind_button.Justify = FBTextJustify.kFBTextJustifyCenter
    ctrlBind_button.Look = FBButtonLook.kFBLookNormal
    ctrlBind_button.OnClick.Add(BtnCallbackctrlBind_button)

    x = FBAddRegionParam(140,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(155,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(45,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("ctrlBake_button","ctrlBake_button", x, y, w, h)

    t.SetControl("ctrlBake_button", ctrlBake_button)
    ctrlBake_button.Visible = True
    ctrlBake_button.ReadOnly = False
    ctrlBake_button.Enabled = True
    ctrlBake_button.Hint = "Bake Selected Bone Chain Anim To Controllers"
    ctrlBake_button.Caption = "Bake"
    ctrlBake_button.State = 0
    ctrlBake_button.Style = FBButtonStyle.kFBPushButton
    ctrlBake_button.Justify = FBTextJustify.kFBTextJustifyCenter
    ctrlBake_button.Look = FBButtonLook.kFBLookNormal
    ctrlBake_button.OnClick.Add(BtnCallbackctrlBake_button)
    
    x = FBAddRegionParam(230,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(200,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(80,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    t.AddRegion("apply_button","apply_button", x, y, w, h)

    t.SetControl("apply_button", apply_button)
    apply_button.Visible = True
    apply_button.ReadOnly = False
    apply_button.Enabled = True
    apply_button.Hint = ""
    apply_button.Caption = "Apply"
    apply_button.State = 0
    apply_button.Style = FBButtonStyle.kFBPushButton
    apply_button.Justify = FBTextJustify.kFBTextJustifyCenter
    apply_button.Look = FBButtonLook.kFBLookNormal
    apply_button.OnClick.Add(BtnCallbackapply_button)
    
    x = FBAddRegionParam(255,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(225,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(55,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    t.AddRegion("ver_lable","ver_lable", x, y, w, h)

    t.SetControl("ver_lable", ver_lable)
    ver_lable.Visible = True
    ver_lable.ReadOnly = True
    ver_lable.Enabled = True
    ver_lable.Hint = ""
    ver_lable.Caption = 'v '+str(version)
    ver_lable.Style = FBTextStyle.kFBTextStyleNone
    ver_lable.Justify = FBTextJustify.kFBTextJustifyRight
    ver_lable.WordWrap = False
    
    x = FBAddRegionParam(15,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(200,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(60,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(24,FBAttachType.kFBAttachNone,"")
    t.AddRegion("Author_button","Author_button", x, y, w, h)

    t.SetControl("Author_button", Author_button)
    Author_button.Visible = True
    Author_button.ReadOnly = False
    Author_button.Enabled = True
    Author_button.Hint = ""
    Author_button.Caption = "@Author"
    Author_button.State = 0
    Author_button.Style = FBButtonStyle.kFBPushButton
    Author_button.Justify = FBTextJustify.kFBTextJustifyCenter
    Author_button.Look = FBButtonLook.kFBLookNormal
    Author_button.OnClick.Add(BtnCallbackAuthor_button)

    x = FBAddRegionParam(95,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(200,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(60,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(24,FBAttachType.kFBAttachNone,"")
    t.AddRegion("wind_button","wind_button", x, y, w, h)

    t.SetControl("wind_button", wind_button)
    wind_button.Visible = True
    wind_button.ReadOnly = False
    wind_button.Enabled = True
    wind_button.Hint = ""
    wind_button.Caption = "+ Wind"
    wind_button.State = 0
    wind_button.Style = FBButtonStyle.kFBPushButton
    wind_button.Justify = FBTextJustify.kFBTextJustifyCenter
    wind_button.Look = FBButtonLook.kFBLookNormal
    wind_button.OnClick.Add(BtnCallbackwind_button)

    x = FBAddRegionParam(110,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(85,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(24,FBAttachType.kFBAttachNone,"")
    t.AddRegion("addBody_button","addBody_button", x, y, w, h)

    t.SetControl("addBody_button", addBody_button)
    addBody_button.Visible = True
    addBody_button.ReadOnly = False
    addBody_button.Enabled = True
    addBody_button.Hint = "Create collision body, will match to selected object"
    addBody_button.Caption = "+"
    addBody_button.State = 0
    addBody_button.Style = FBButtonStyle.kFBPushButton
    addBody_button.Justify = FBTextJustify.kFBTextJustifyCenter
    addBody_button.Look = FBButtonLook.kFBLookNormal
    addBody_button.OnClick.Add(BtnCallbackaddBody_button)

    x = FBAddRegionParam(140,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(85,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(24,FBAttachType.kFBAttachNone,"")
    t.AddRegion("deleteBody_button","deleteBody_button", x, y, w, h)

    t.SetControl("deleteBody_button", deleteBody_button)
    deleteBody_button.Visible = True
    deleteBody_button.ReadOnly = False
    deleteBody_button.Enabled = True
    deleteBody_button.Hint = "Remove selected collision body"
    deleteBody_button.Caption = "-"
    deleteBody_button.State = 0
    deleteBody_button.Style = FBButtonStyle.kFBPushButton
    deleteBody_button.Justify = FBTextJustify.kFBTextJustifyCenter
    deleteBody_button.Look = FBButtonLook.kFBLookNormal
    deleteBody_button.OnClick.Add(BtnCallbackdeleteBody_button)

    x = FBAddRegionParam(170,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(85,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(50,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(24,FBAttachType.kFBAttachNone,"")
    t.AddRegion("removeAllBody_button","removeAllBody_button", x, y, w, h)

    t.SetControl("removeAllBody_button", removeAllBody_button)
    removeAllBody_button.Visible = True
    removeAllBody_button.ReadOnly = False
    removeAllBody_button.Enabled = True
    removeAllBody_button.Hint = "Clear all collision body in scene"
    removeAllBody_button.Caption = "Clear"
    removeAllBody_button.State = 0
    removeAllBody_button.Style = FBButtonStyle.kFBPushButton
    removeAllBody_button.Justify = FBTextJustify.kFBTextJustifyCenter
    removeAllBody_button.Look = FBButtonLook.kFBLookNormal
    removeAllBody_button.OnClick.Add(BtnCallbackremoveAllBody_button)




def CreateTool():
    t = FBCreateUniqueTool("Spring Magic in MB         Yanbin Bai")
    t.StartSizeX = 340
    t.StartSizeY = 265
    PopulateTool(t)
    ShowTool(t)
    return t

warning_text = FBLabel()
mail_edit = FBEdit()

def PopulateWarning(t):
    #populate regions here

    x = FBAddRegionParam(10,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(20,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(270,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(70,FBAttachType.kFBAttachNone,"")
    t.AddRegion("warning_text","warning_text", x, y, w, h)

    t.SetControl("warning_text", warning_text)
    warning_text.Visible = True
    warning_text.ReadOnly = True
    warning_text.Enabled = True
    warning_text.Hint = ""
    warning_text.Caption = "This tool can only be used on authored computer!\n\nPlease contact                          for more details!"
    warning_text.Style = FBTextStyle.kFBTextStyleNone
    warning_text.Justify = FBTextJustify.kFBTextJustifyCenter
    warning_text.WordWrap = True
    
    x = FBAddRegionParam(100,FBAttachType.kFBAttachNone,"")
    y = FBAddRegionParam(50,FBAttachType.kFBAttachNone,"")
    w = FBAddRegionParam(140,FBAttachType.kFBAttachNone,"")
    h = FBAddRegionParam(20,FBAttachType.kFBAttachNone,"")
    t.AddRegion("mail_edit","mail_edit", x, y, w, h)

    t.SetControl("mail_edit", mail_edit)
    mail_edit.Visible = True
    mail_edit.ReadOnly = False
    mail_edit.Enabled = True
    mail_edit.Hint = ""
    mail_edit.Text = email
    mail_edit.PasswordMode = False
    
def CreateWarning():
    tt = FBCreateUniqueTool("Warning")
    tt.StartSizeX = 300
    tt.StartSizeY = 150
    PopulateWarning(tt)
    ShowTool(tt)


if __name__ == "__main__":
    CreateTool()
    # checkUpdate()


