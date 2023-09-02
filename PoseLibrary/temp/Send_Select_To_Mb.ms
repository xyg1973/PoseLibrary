rollout unnamedRollout "Send to MoBu" width:163 height:54
(
    button 'btn1' "send to motionbuilder" pos:[7,8] width:148 height:37 align:#left
    on btn1 pressed do
    (
        global exportName
        global starttime = animationRange.start
        global endtime = animationRange.end
        function selectHierarchy =(
            for p in selection do(
                
            if p.children != undefined do
            (
            selectmore p.children
            )
            )
        )
        
        
        function fbxexportA =(
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
        
        
        
        
        function fbximportA =(
            global exportName
            ---导入FBX
            --To import an fbx file using the 'Add to new scene' mode,
            --the skin modifier but preventing the loading of animation:
            FBXImporterSetParam "Mode" #create
            FBXImporterSetParam "Skin" true
            FBXImporterSetParam "FillTimeline" true
            FBXImporterSetParam "BakeAnimationLayers" true
            FBXImporterSetParam "PointCache" false
            FBXImporterSetParam "Animation" true
            FBXImporterSetParam "ImportBoneAsDummy" false
            
            
            importfile exportName #noPrompt using:FBXIMP
        )
        
        
        
        sceneName = maxFilePath + maxFileName
        if sceneName =="" do sceneName = sysInfo.tempdir+"Temp.FBX"
        scenepathA =getFilenamePath sceneName
        fileNameA = getFilenameFile sceneName
        exportName = scenepathA+fileNameA+".FBX"
        
        
        if $root != undefined do (
            select $root
            selectHierarchy()
            fbxexportA()
        
            ---新建场景
            resetMaxFile #noprompt
        
            fbximportA()
        
            select $root
            actionMan.executeAction 853085736 "1"  -- One Click MotionBuilder: Update Current Scene to MotionBuilder
        )
    )
)
CreateDialog unnamedRollout pos:[800, 400] 