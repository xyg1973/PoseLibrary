macroScript updateScene
category:"SN_AnimTool"
tooltip:"更新场景"
(
    function fbximportA =(

        ---导入FBX
        --To import an fbx file using the 'Add to new scene' mode,
        --the skin modifier but preventing the loading of animation:
        --FBXImporterSetParam "Mode"  # create
        FBXImporterSetParam "Skin" true
        FBXImporterSetParam "FillTimeline" true
        FBXImporterSetParam "BakeAnimationLayers" true
        FBXImporterSetParam "PointCache" false
        FBXImporterSetParam "Animation" true
        FBXImporterSetParam "ImportBoneAsDummy" false
    )

    basePath= "C:/Users/"
    userName=sysInfo.username
    TempFilePath = basePath+userName+"/"+"Documents/SN AnimTool/SendTemp_Mb.fbx"

    fbximportA()
    try (importfile TempFilePath #noPrompt using:FBXIMP) catch()

    print "更新场景"
)

macroScript fix_bip_porp
category:"SN_AnimTool"
tooltip:"修正porp"
(
    bip_porp1  = $'port1_temp'
   -- bip_porp2  = $'port2_temp'
    bip_porp1.parent =  $Bip001
    --bip_porp2.parent =  $Bip001

    point_porp1 =  $'Bip001 Prop1'
    --point_porp2 =  $'Bip001 Prop2'

    starttime = animationRange.start
    endtime = animationRange.end
    set animate on
    with animate on
    sliderTime = starttime
    for t = starttime to endtime do (at time t
        bip_porp1.transform = point_porp1.transform
       -- bip_porp2.transform = point_porp2.transform
        sliderTime += 1
        )


    delete point_porp1
   -- delete point_porp2

    bip_porp1.name = "Bip001 Prop1"
   -- bip_porp2.name = "Bip001 Prop2"
)

macroScript revise_bip_porp
category:"SN_AnimTool"
tooltip:"修改porp类型"
(
    bip_porp1 =  $'Bip001 Prop1'
    --bip_porp2 =  $'Bip001 Prop2'
    bip_porp1.name = "port1_temp"
    --bip_porp2.name = "port2_temp"


    point_porp1 = Point pos:[0,0,0] isSelected:off
    point_porp1.name = "Bip001 Prop1"
    point_porp1.parent = $Bip001

    --point_porp2 = Point pos:[0,0,0] isSelected:off
    --point_porp2.name = "Bip001 Prop2"
   -- point_porp2.parent = $Bip001

    bip_porp1.parent = point_porp1
   -- bip_porp2.parent = point_porp2
)

macroScript Send_Select_To_MB
category:"SN_AnimTool"
tooltip:"发送到MB"
(

global exportName
global starttime = animationRange.start
global endtime = animationRange.end

function selectHierarchy =(
        for p in selection do(
                if p.children != undefined do (selectmore p.children)
        )
    )

function fbxexport = (
    global exportName
    global starttime
    global endtime


    ---导出FBX
    FBXExporterSetParam "ASCII" true
    --to prevent the export of the cameras:
    FBXExporterSetParam "Cameras" False
    FBXExporterSetParam "BakeAnimation" true
    FBXExporterSetParam "BakeFrameStart" starttime
    FBXExporterSetParam "BakeFrameEnd" endtime
    FBXExporterSetParam "BakeFrameStep" 1
    FBXExporterSetParam "UpAxis" "Y"
    exportFile exportName #noPrompt selectedOnly:true using:FBXEXP
)
fn createDirStructure dir =
 	(
 		local a = filterString dir "\\/"
 		local str = ""
 		for i in a do
 		(
 			str += i + "\\"
 			makeDir str
 		)
 		str
 	)


basePath= "C:/Users/"
userName=sysInfo.username
TempFileFolder = basePath+userName+"/"+"Documents/SN AnimTool"
--"创建文件夹"
createDirStructure(TempFileFolder)
TempFilePath = TempFileFolder+"/SendTemp_Max.fbx"
exportName = TempFilePath
if $root != undefined do (
    select $root
    selectHierarchy()
    fbxexport()
	print "发送成功"
)
)


macroScript PoseLibrary
category:"SN_AnimTool"
tooltip:"pose库"
(
Maxpath = GetDir #maxroot
poselibrayPath = Maxpath +"\python\PoseLibrary\\run.py"
python.ExecuteFile poselibrayPath
)


SN_AnimTool_Menu = menuMan.findMenu "SN_AnimTool"

try (menuMan.unregisterMenu SN_AnimTool_Menu) catch()

--"创建SN_AnimToolItem"
theMainMenu = menuMan.getMainMenuBar()
SN_AnimTool_Menu = menuMan.createMenu "SN_AnimTool"
SN_AnimTool_SubMenu = menuMan.createSubMenuItem "SN_AnimTool" SN_AnimTool_Menu
theMainMenu.addItem SN_AnimTool_SubMenu (theMainMenu.numItems()+1)

--"创建RigItem"
Rig_Menu = menuMan.createMenu "绑定"
Rig_SubMenu = menuMan.createSubMenuItem "绑定" Rig_Menu
SN_AnimTool_Menu.addItem Rig_SubMenu (SN_AnimTool_Menu.numItems() + 1)

--"创建AnimItem"
Anim_Menu = menuMan.createMenu "动画"
Anim_SubMenu = menuMan.createSubMenuItem "动画" Anim_Menu
SN_AnimTool_Menu.addItem Anim_SubMenu (SN_AnimTool_Menu.numItems()+1)


--"创建一个更新场景的 ActionItem MacroScript 到 SN_AnimTool"
UpdateSceneAction = menuMan.createActionItem "updateScene" "SN_AnimTool"
SN_AnimTool_Menu.addItem UpdateSceneAction (SN_AnimTool_Menu.numItems()+1)

--"创建一个发送到MB的 ActionItem MacroScript 到 SN_AnimTool"
Send_Select_TO_MB = menuMan.createActionItem "Send_Select_To_MB" "SN_AnimTool"
SN_AnimTool_Menu.addItem Send_Select_TO_MB (SN_AnimTool_Menu.numItems()+1)

--"创建更新场景前修复武器骨骼类型 ActionItem MacroScript 到 SN_AnimTool"
revise_bip_porp = menuMan.createActionItem "revise_bip_porp" "SN_AnimTool"
SN_AnimTool_Menu.addItem revise_bip_porp (SN_AnimTool_Menu.numItems()+1)

--"创建更新场景后还原武器骨骼动画 ActionItem MacroScript 到 SN_AnimTool"
fix_bip_porp = menuMan.createActionItem "fix_bip_porp" "SN_AnimTool"
SN_AnimTool_Menu.addItem fix_bip_porp (SN_AnimTool_Menu.numItems()+1)

--"创建一个Pose库的 ActionItem MacroScript 到 SN_AnimTool-Anim"
PoseLibraryAction = menuMan.createActionItem "PoseLibrary" "SN_AnimTool"
Anim_Menu.addItem PoseLibraryAction  (Anim_Menu.numItems()+1)

--"更新max菜单"
menuMan.updateMenuBar()

