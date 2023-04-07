# -*- coding: utf-8 -*-
import pyfbsdk as fb
import pyfbsdk_additions as fba
 
def GetCurrentFrame():
    Frame = fb.FBSystem().LocalTime.GetFrame()
    return Frame
 
def GotoFrame(time):
    t = fb.FBTime(0, 0, 0, time, 0)
    fb.FBPlayerControl().Goto(t)
 
##Check For Conflicts In User's Desired Frame Ranges
def FrameCheck():
    ##Does Blend In Conflict With Start Frame
    if nBlendIn.Value > nStart.Value:
        fb.FBMessageBox( "Frame Input Error", "Blend In Frame Is Higher Than The Start Frame", "OK" )
        return False
    ##Does Start Frame Conflict Wtih End Frame
    if nEnd.Value < nStart.Value:
        fb.FBMessageBox( "Frame Input Error", "End Frame Is Lower Than The Start Frame", "OK" )
        return False
    ##Does Blend Out Frame Conflict With End Frame
    if nBlendOut.Value < nEnd.Value:
        fb.FBMessageBox( "Frame Input Error", "Blend Out Frame Is Lower Than The End Frame", "OK" )
        return False
    else:
        return True
 
##Get Selected Object
def GetSelObj():
    ModelList = fb.FBModelList()
    fb.FBGetSelectedModels(ModelList, None, True, True)
    if len(ModelList) == 1:
        for Model in ModelList:
            SelObjName = Model.LongName
        return SelObjName
    else:
        fb.FBMessageBox( "Object Select Error", "Please Selecte An Object", "OK" )
 
##Get Layer Count
def GetLayerCount():
    return fb.FBSystem().CurrentTake.GetLayerCount()
 
##Zero The Translation and Rotation Of The Selected Object
def ZeroTRTransforms(YourObject):
    YourObject.Translation = fb.FBVector3d()
    YourObject.Rotation = fb.FBVector3d()
 
##Create The Layer We Will Work On
def CreateLayer():
    SelObj = GetSelObj()#.rsplit(':', 2)[2]
    fb.FBSystem().CurrentTake.CreateNewLayer()
    ##Set the new layer as the current one (Keys will be added to that layer)
    lCount = fb.FBSystem().CurrentTake.GetLayerCount()
    ##Name the Layer to be "Selected Object Name: Start Frame to End Frame" (ie. LeftHeelPivot: 100-150)
    fb.FBSystem().CurrentTake.GetLayer(lCount-1).Name = SelObj + " " + str( int(nStart.Value) ) + "-" + str( int(nEnd.Value) )
    fb.FBSystem().CurrentTake.SetCurrentLayer(lCount-1)
 
##Enure That Blend In, Ref Pose and Blend Out Translation And Roation Are Preserved
def PreserveFrames():
    ##Create A List Of Frame That We Want ZeroKeys To Be Set On
    ZeroFrames = ( int(nBlendIn.Value), int(nRef.Value), int(nBlendOut.Value) )
    ##Get Selected Object
    YourObject = GetSelObj()
    for FrameNumber in ZeroFrames:
        GotoFrame(FrameNumber)
        fb.FBPlayerControl().Key()
 
##For Each Frame Between The Defind Start Frame And End Frame We Will Create A Key
##And Match The Translation And Rotation To That Of The Values On The RefPose Frame
def MatchRefPose():
    GotoFrame( int(nRef.Value) )
    MyObject = GetSelObj()
    RefObjTrans = fb.FBVector3d()
    RefObjRot = fb.FBVector3d()
    fb.FBFindModelByLabelName(MyObject).GetVector (RefObjTrans, fb.FBModelTransformationType.kModelTranslation, False)
    fb.FBFindModelByLabelName(MyObject).GetVector (RefObjRot, fb.FBModelTransformationType.kModelRotation, False)
    GotoFrame( int(nStart.Value) )
 
    lval = ( int(nEnd.Value) - int(nStart.Value) )
    lprogsum = 1
    lpercent = (100.0/lval)
 
    for time in range ( int(nStart.Value), int(nEnd.Value) ):
        if time == int(nRef.Value):
            pass
        else:
            GotoFrame(time)
            if bTR.State == 1:
                fb.FBFindModelByLabelName(MyObject).Translation = RefObjTrans
                fb.FBFindModelByLabelName(MyObject).Rotation = RefObjRot
                fb.FBPlayerControl().Key()
            if bTrans.State == 1:
                if bTX.State == 1:
                    lTX = RefObjTrans[0]
                if bTX.State != 1:
                    lTX = fb.FBFindModelByLabelName(MyObject).Translation[0]
                if bTY.State == 1:
                    lTY = RefObjTrans[1]
                if bTY.State != 1:
                    lTY = fb.FBFindModelByLabelName(MyObject).Translation[1]
                if bTZ.State == 1:
                    lTZ = RefObjTrans[2]
                if bTZ.State != 1:
                    lTZ = fb.FBFindModelByLabelName(MyObject).Translation[2]
                fb.FBFindModelByLabelName(MyObject).Translation = fb.FBVector3d(lTX, lTY, lTZ)
                fb.FBPlayerControl().Key()
            if bRot.State == 1:
                if bRX.State == 1:
                    lRX = RefObjRot[0]
                if bRX.State != 1:
                    lRX = fb.FBFindModelByLabelName(MyObject).Rotation[0]
                if bRY.State == 1:
                    lRY = RefObjRot[1]
                if bRY.State != 1:
                    lRY = fb.FBFindModelByLabelName(MyObject).Rotation[1]
                if bRZ.State == 1:
                    lRZ = RefObjRot[2]
                if bRZ.State != 1:
                    lRZ = fb.FBFindModelByLabelName(MyObject).Rotation[2]
                fb.FBFindModelByLabelName(MyObject).Rotation = fb.FBVector3d(lRX, lRY, lRZ)
                fb.FBPlayerControl().Key()
 
##UI Starts Here
 
hBlendIn = fb.FBLabel()
nBlendIn = fb.FBEditNumber()
bBlendIn = fb.FBButton()
hBlendOut = fb.FBLabel()
nBlendOut = fb.FBEditNumber()
bBlendOut = fb.FBButton()
hStart = fb.FBLabel()
nStart = fb.FBEditNumber()
bStart = fb.FBButton()
hEnd = fb.FBLabel()
nEnd = fb.FBEditNumber()
bEnd = fb.FBButton()
hRef = fb.FBLabel()
nRef = fb.FBEditNumber()
bRef = fb.FBButton()
bTR = fb.FBButton()
bTrans = fb.FBButton()
bTX = fb.FBButton()
bTY = fb.FBButton()
bTZ = fb.FBButton()
bRot = fb.FBButton()
bRX = fb.FBButton()
bRY = fb.FBButton()
bRZ = fb.FBButton()
bStopSliding = fb.FBButton()
 
##Get Current Frame For Blend In Time
def bBlendInCallBack(control, event):
    CurrentFrame = GetCurrentFrame()
    nBlendIn.Value = CurrentFrame
 
##Get Current Frame For Blend Out Time
def bBlendOutCallBack(control, event):
    CurrentFrame = GetCurrentFrame()
    nBlendOut.Value = CurrentFrame
 
##Get Current Frame For Start Time
def bStartCallBack(control, event):
    CurrentFrame = GetCurrentFrame()
    nStart.Value = CurrentFrame
 
##Get Current Frame For End Time
def bBlendEndCallBack(control, event):
    CurrentFrame = GetCurrentFrame()
    nEnd.Value = CurrentFrame
 
##Get Current Frame For Reference Pose Time
def bBlendRefCallBack(control, event):
    CurrentFrame = GetCurrentFrame()
    nRef.Value = CurrentFrame
 
##Match Translation and Rotation Transforms
def bTRCallBack(control, event):
    if bTR.State == 1:
        bTrans.Enabled = bTX.Enabled = bTY.Enabled = bTZ.Enabled = bRot.Enabled = bRX.Enabled = bRY.Enabled = bRZ.Enabled = False
        bTrans.State = bTX.State = bTY.State = bTZ.State = bRot.State = bRX.State = bRY.State = bRZ.State = False
    else:
        bTrans.Enabled = bTX.Enabled = bTY.Enabled = bTZ.Enabled = bRot.Enabled = bRX.Enabled = bRY.Enabled = bRZ.Enabled = True
        bTrans.State = bTX.State = bTY.State = bTZ.State = True
 
##Match Translation Transforms
def bTransCallBack(control, event):
    if bTrans.State == 0:
        bTX.State = bTY.State = bTZ.State = 0
    else:
        bTX.State = bTY.State = bTZ.State = 1
 
##Match Rotation Transforms
def bRotCallBack(control, event):
    if bRot.State == 0:
        bRX.State = bRY.State = bRZ.State = 0
    else:
        bRX.State = bRY.State = bRZ.State = 1
 
##Stop Sliding
def bStopSlidingCallBack(control, event):
    ##Check That There Is No Conflicts Between Inputs Blend In Frame, Start Frame, End Frame and Blend Out Frame
    Process = FrameCheck()
    if Process == True:
        if bTR.State != 1 and bTrans.State != 1 and bRot.State != 1:
            fb.FBMessageBox( "Transform Match Error", "Please Select Which Transforms To Match", "OK" )
            pass
        else:
            ##Get Users Frame They Were On When Executing The Stop Sliding Button
            OrgFrame = GetCurrentFrame()
            ##Get Layer Count So We Can Later Compare
            lOrgLayCount = GetLayerCount()
            ##If The User Has An Object Selected Create A New Layer Named After That Object And The Frames Inputed
            CreateLayer()
            ##Fail Safe To See If The Layer Was Created
            lCurLayCount = GetLayerCount()
            ##If All Is Good
            if lCurLayCount > lOrgLayCount:
                PreserveFrames()
                MatchRefPose()
                GotoFrame(OrgFrame)
            ##If Stop Sliding Layer Was Not Able To Be Created
            else:
               GotoFrame(OrgFrame)
               fb.FBMessageBox( "Could Not Process", "Please Ensure That A Foot Was Selected And Try Again", "OK" )
    else:
      fb.FBMessageBox( "Could Not Process", "Please Check The Frames You Have Inputed", "OK" )  
 
def PopulateTool(t):
    #populate regions here
 
    x = fb.FBAddRegionParam(5,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(10,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(105,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(15,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("hBlendIn","hBlendIn", x, y, w, h)
 
    t.SetControl("hBlendIn", hBlendIn)
    hBlendIn.Visible = True
    hBlendIn.ReadOnly = False
    hBlendIn.Enabled = True
    hBlendIn.Hint = ""
    hBlendIn.Caption = "Blend In Frame"
    hBlendIn.Style = fb.FBTextStyle.kFBTextStyleNone
    hBlendIn.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    hBlendIn.WordWrap = False
 
    x = fb.FBAddRegionParam(5,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(25,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(75,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("nBlendIn","nBlendIn", x, y, w, h)
 
    t.SetControl("nBlendIn", nBlendIn)
    nBlendIn.Visible = True
    nBlendIn.ReadOnly = False
    nBlendIn.Enabled = True
    nBlendIn.Hint = ""
    nBlendIn.Value = 0.000000
 
    x = fb.FBAddRegionParam(80,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(25,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bBlendIn","bBlendIn", x, y, w, h)
 
    t.SetControl("bBlendIn", bBlendIn)
    bBlendIn.Visible = True
    bBlendIn.ReadOnly = False
    bBlendIn.Enabled = True
    bBlendIn.Hint = "Use Current Frame"
    bBlendIn.Caption = "{]"
    bBlendIn.State = 0
    bBlendIn.Style = fb.FBButtonStyle.kFBPushButton
    bBlendIn.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    bBlendIn.Look = fb.FBButtonLook.kFBLookNormal
    bBlendIn.OnClick.Add(bBlendInCallBack) 
 
    x = fb.FBAddRegionParam(145,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(10,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(105,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(15,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("hBlendOut","hBlendOut", x, y, w, h)
 
    t.SetControl("hBlendOut", hBlendOut)
    hBlendOut.Visible = True
    hBlendOut.ReadOnly = False
    hBlendOut.Enabled = True
    hBlendOut.Hint = ""
    hBlendOut.Caption = "Blend Out Frame"
    hBlendOut.Style = fb.FBTextStyle.kFBTextStyleNone
    hBlendOut.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    hBlendOut.WordWrap = False
 
    x = fb.FBAddRegionParam(145,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(25,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(75,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("nBlendOut","nBlendOut", x, y, w, h)
 
    t.SetControl("nBlendOut", nBlendOut)
    nBlendOut.Visible = True
    nBlendOut.ReadOnly = False
    nBlendOut.Enabled = True
    nBlendOut.Hint = ""
    nBlendOut.Value = 0.000000
 
    x = fb.FBAddRegionParam(220,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(25,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bBlendOut","bBlendOut", x, y, w, h)
 
    t.SetControl("bBlendOut", bBlendOut)
    bBlendOut.Visible = True
    bBlendOut.ReadOnly = False
    bBlendOut.Enabled = True
    bBlendOut.Hint = "Use Current Frame"
    bBlendOut.Caption = "{]"
    bBlendOut.State = 0
    bBlendOut.Style = fb.FBButtonStyle.kFBPushButton
    bBlendOut.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    bBlendOut.Look = fb.FBButtonLook.kFBLookNormal
    bBlendOut.OnClick.Add(bBlendOutCallBack) 
 
    x = fb.FBAddRegionParam(5,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(65,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(105,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(15,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("hStart","hStart", x, y, w, h)
 
    t.SetControl("hStart", hStart)
    hStart.Visible = True
    hStart.ReadOnly = False
    hStart.Enabled = True
    hStart.Hint = ""
    hStart.Caption = "Start Frame"
    hStart.Style = fb.FBTextStyle.kFBTextStyleNone
    hStart.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    hStart.WordWrap = False
 
    x = fb.FBAddRegionParam(5,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(80,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(75,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("nStart","nStart", x, y, w, h)
 
    t.SetControl("nStart", nStart)
    nStart.Visible = True
    nStart.ReadOnly = False
    nStart.Enabled = True
    nStart.Hint = ""
    nStart.Value = 0.000000
 
    x = fb.FBAddRegionParam(80,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(80,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bStart","bStart", x, y, w, h)
 
    t.SetControl("bStart", bStart)
    bStart.Visible = True
    bStart.ReadOnly = False
    bStart.Enabled = True
    bStart.Hint = "Use Current Frame"
    bStart.Caption = "{]"
    bStart.State = 0
    bStart.Style = fb.FBButtonStyle.kFBPushButton
    bStart.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    bStart.Look = fb.FBButtonLook.kFBLookNormal
    bStart.OnClick.Add(bStartCallBack) 
 
    x = fb.FBAddRegionParam(145,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(65,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(105,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(15,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("hEnd","hEnd", x, y, w, h)
 
    t.SetControl("hEnd", hEnd)
    hEnd.Visible = True
    hEnd.ReadOnly = False
    hEnd.Enabled = True
    hEnd.Hint = ""
    hEnd.Caption = "End Frame"
    hEnd.Style = fb.FBTextStyle.kFBTextStyleNone
    hEnd.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    hEnd.WordWrap = False
 
    x = fb.FBAddRegionParam(145,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(80,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(75,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("nEnd","nEnd", x, y, w, h)
 
    t.SetControl("nEnd", nEnd)
    nEnd.Visible = True
    nEnd.ReadOnly = False
    nEnd.Enabled = True
    nEnd.Hint = ""
    nEnd.Value = 0.000000
 
    x = fb.FBAddRegionParam(220,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(80,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bEnd","bEnd", x, y, w, h)
 
    t.SetControl("bEnd", bEnd)
    bEnd.Visible = True
    bEnd.ReadOnly = False
    bEnd.Enabled = True
    bEnd.Hint = "Use Current Frame"
    bEnd.Caption = "{]"
    bEnd.State = 0
    bEnd.Style = fb.FBButtonStyle.kFBPushButton
    bEnd.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    bEnd.Look = fb.FBButtonLook.kFBLookNormal
    bEnd.OnClick.Add(bBlendEndCallBack) 
 
    x = fb.FBAddRegionParam(75,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(120,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(105,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(15,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("hRef","hRef", x, y, w, h)
 
    t.SetControl("hRef", hRef)
    hRef.Visible = True
    hRef.ReadOnly = False
    hRef.Enabled = True
    hRef.Hint = ""
    hRef.Caption = "Reference Frame"
    hRef.Style = fb.FBTextStyle.kFBTextStyleBold
    hRef.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    hRef.WordWrap = False
 
    x = fb.FBAddRegionParam(75,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(135,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(75,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("nRef","nRef", x, y, w, h)
 
    t.SetControl("nRef", nRef)
    nRef.Visible = True
    nRef.ReadOnly = False
    nRef.Enabled = True
    nRef.Hint = ""
    nRef.Value = 0.000000
 
    x = fb.FBAddRegionParam(150,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(135,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bRef","bRef", x, y, w, h)
 
    t.SetControl("bRef", bRef)
    bRef.Visible = True
    bRef.ReadOnly = False
    bRef.Enabled = True
    bRef.Hint = "Use Current Frame"
    bRef.Caption = "{]"
    bRef.State = 0
    bRef.Style = fb.FBButtonStyle.kFBPushButton
    bRef.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    bRef.Look = fb.FBButtonLook.kFBLookNormal
    bRef.OnClick.Add(bBlendRefCallBack) 
 
    x = fb.FBAddRegionParam(5,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(185,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(40,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(25,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bTR","bTR", x, y, w, h)
 
    t.SetControl("bTR", bTR)
    bTR.Visible = True
    bTR.ReadOnly = False
    bTR.Enabled = True
    bTR.Hint = "Affect Translation And Rotation"
    bTR.Caption = "TR"
    bTR.State = 0
    bTR.Style = fb.FBButtonStyle.kFBCheckbox
    bTR.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bTR.Look = fb.FBButtonLook.kFBLookNormal
    bTR.OnClick.Add(bTRCallBack) 
 
    x = fb.FBAddRegionParam(60,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(185,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(90,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(25,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bTrans","bTrans", x, y, w, h)
 
    t.SetControl("bTrans", bTrans)
    bTrans.Visible = True
    bTrans.ReadOnly = False
    bTrans.Enabled = True
    bTrans.Hint = "Affect Translation"
    bTrans.Caption = "Translation"
    bTrans.State = 1
    bTrans.Style = fb.FBButtonStyle.kFBCheckbox
    bTrans.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bTrans.Look = fb.FBButtonLook.kFBLookNormal
    bTrans.OnClick.Add(bTransCallBack) 
 
    x = fb.FBAddRegionParam(60,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(210,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bTX","bTX", x, y, w, h)
 
    t.SetControl("bTX", bTX)
    bTX.Visible = True
    bTX.ReadOnly = False
    bTX.Enabled = True
    bTX.Hint = ""
    bTX.Caption = "X"
    bTX.State = 1
    bTX.Style = fb.FBButtonStyle.kFBCheckbox
    bTX.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bTX.Look = fb.FBButtonLook.kFBLookNormal
 
    x = fb.FBAddRegionParam(90,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(210,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bTY","bTY", x, y, w, h)
 
    t.SetControl("bTY", bTY)
    bTY.Visible = True
    bTY.ReadOnly = False
    bTY.Enabled = True
    bTY.Hint = ""
    bTY.Caption = "Y"
    bTY.State = 1
    bTY.Style = fb.FBButtonStyle.kFBCheckbox
    bTY.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bTY.Look = fb.FBButtonLook.kFBLookNormal
 
    x = fb.FBAddRegionParam(120,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(210,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bTZ","bTZ", x, y, w, h)
 
    t.SetControl("bTZ", bTZ)
    bTZ.Visible = True
    bTZ.ReadOnly = False
    bTZ.Enabled = True
    bTZ.Hint = ""
    bTZ.Caption = "Z"
    bTZ.State = 1
    bTZ.Style = fb.FBButtonStyle.kFBCheckbox
    bTZ.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bTZ.Look = fb.FBButtonLook.kFBLookNormal
 
    x = fb.FBAddRegionParam(160,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(185,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(90,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(25,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bRot","bRot", x, y, w, h)
 
    t.SetControl("bRot", bRot)
    bRot.Visible = True
    bRot.ReadOnly = False
    bRot.Enabled = True
    bRot.Hint = ""
    bRot.Caption = "Rotation"
    bRot.State = 0
    bRot.Style = fb.FBButtonStyle.kFBCheckbox
    bRot.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bRot.Look = fb.FBButtonLook.kFBLookNormal
    bRot.OnClick.Add(bRotCallBack) 
 
    x = fb.FBAddRegionParam(160,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(210,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bRX","bRX", x, y, w, h)
 
    t.SetControl("bRX", bRX)
    bRX.Visible = True
    bRX.ReadOnly = False
    bRX.Enabled = True
    bRX.Hint = ""
    bRX.Caption = "X"
    bRX.State = 0
    bRX.Style = fb.FBButtonStyle.kFBCheckbox
    bRX.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bRX.Look = fb.FBButtonLook.kFBLookNormal 
 
    x = fb.FBAddRegionParam(190,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(210,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bRY","bRY", x, y, w, h)
 
    t.SetControl("bRY", bRY)
    bRY.Visible = True
    bRY.ReadOnly = False
    bRY.Enabled = True
    bRY.Hint = ""
    bRY.Caption = "Y"
    bRY.State = 0
    bRY.Style = fb.FBButtonStyle.kFBCheckbox
    bRY.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bRY.Look = fb.FBButtonLook.kFBLookNormal 
 
    x = fb.FBAddRegionParam(220,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(210,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(30,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bRZ","bRZ", x, y, w, h)
 
    t.SetControl("bRZ", bRZ)
    bRZ.Visible = True
    bRZ.ReadOnly = False
    bRZ.Enabled = True
    bRZ.Hint = ""
    bRZ.Caption = "Z"
    bRZ.State = 0
    bRZ.Style = fb.FBButtonStyle.kFBCheckbox
    bRZ.Justify = fb.FBTextJustify.kFBTextJustifyLeft
    bRZ.Look = fb.FBButtonLook.kFBLookNormal
 
    x = fb.FBAddRegionParam(0,fb.FBAttachType.kFBAttachNone,"")
    y = fb.FBAddRegionParam(270,fb.FBAttachType.kFBAttachNone,"")
    w = fb.FBAddRegionParam(255,fb.FBAttachType.kFBAttachNone,"")
    h = fb.FBAddRegionParam(50,fb.FBAttachType.kFBAttachNone,"")
    t.AddRegion("bStopSliding","bStopSliding", x, y, w, h)
 
    t.SetControl("bStopSliding", bStopSliding)
    bStopSliding.Visible = True
    bStopSliding.ReadOnly = False
    bStopSliding.Enabled = True
    bStopSliding.Hint = ""
    bStopSliding.Caption = "Stop Sliding"
    bStopSliding.State = 0
    bStopSliding.Style = fb.FBButtonStyle.kFBPushButton
    bStopSliding.Justify = fb.FBTextJustify.kFBTextJustifyCenter
    bStopSliding.Look = fb.FBButtonLook.kFBLookNormal
    bStopSliding.OnClick.Add(bStopSlidingCallBack) 
 
def CreateTool():
    t = fba.FBCreateUniqueTool("Stop Foot Sliding v1.0")
    t.StartSizeX = 270
    t.StartSizeY = 370
    PopulateTool(t)
    fb.ShowTool(t)
    return t

if __name__ == "__main__":
    CreateTool()