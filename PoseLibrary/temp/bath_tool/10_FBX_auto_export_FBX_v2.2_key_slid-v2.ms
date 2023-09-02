--99U:199505
--QQE-mail:738746223@qq.com

--fileIn "key_slid.ms"
rollout rename_File "重命名文件" width:370  height:220
(
    group "目标" (
        edittext form_path "路径"
        checkbox check_fbx ".FBX" across:2
        checkbox check_max ".MAX" offset:[-120,0] checked:true
    )
    group "" (
        checkbox chk_f_text across:2
        edittext f_str "前缀" fieldWidth:280 labelOnTop:false offset:[-140,0]

        checkbox chk_f_text_01 across:3 --前端字符操作
        radiobuttons sele_f_b_text_00 labels:#("保留前","删除前")  columns:2 offset:[-90,0]
        spinner delPreSpin_f  range:[0,20,0] type:#integer offset:[-90,0]

        label lab_01 ""
        checkbox chk_b_text across:2
        edittext b_str "后缀" fieldWidth:280 labelOnTop:false offset:[-140,0]

        /*
        checkbox chk_b_text_01 across:3
        radiobuttons sele_f_b_text_01 labels:#("保留后","删除后")  columns:2 offset:[-90,0]
        spinner delPreSpin_b  range:[0,20,0] type:#integer offset:[-90,0]
        */
    )
    button btn_01 "OK " width:338 height:26--across:2
    --button btn_02 "Ok MAX"
    fn find_file type =     -- 找到 源 路径 文件夹里面的FBX - max 文件，忽略次级目录
    (
        --local from_path = pathSource + @"\"
        if form_path.text != "" then
        (
            local from_path = form_path.text + @"\"
            if type == 1 do (tem_file_fbx = getFiles (from_path + "*"+".FBX");return tem_file_fbx )
            if type == 2 do (tem_file_max = getFiles (from_path + "*"+".max");return tem_file_max )
        )
        else(return undefined)

    )
    fn new_name_file tem_path =
    (
        file_name = getFilenameFile tem_path
        file_path = getFilenamePath tem_path
        file_type = getFilenameType tem_path

        new_name = file_name
        if chk_f_text_01.state == true do  --前端字符操作
        (
            if sele_f_b_text_00.state == 1 then  --保留前几个字符
            (
                new_name = (substring file_name 1 delPreSpin_f.value)
            )
            else
            (   --删除前几个字符
                local start_t = delPreSpin_f.value + 1
                local end_t = file_name.count
                new_name = (substring file_name start_t end_t)
            )
        )

        if chk_f_text.state == true do --添加前缀名
        (
            if f_str.text != "" do ( new_name = f_str.text + new_name )
        )

        if chk_b_text.state == true do --添加后缀名
        (
            if b_str.text != "" do (new_name += b_str.text)
        )
        --new_name = (substring file_name 1 3) + "_o" --取前3个字符
        --new_name = file_name + "_20180823_熊建桥"
        --if new_name != file_name do
        if true do
        (try (
            new_path = file_path + new_name + file_type
            renameFile tem_path new_path;print "oook"
            )catch("OK")
        )
    )

    on btn_01 pressed do
    (
        if check_fbx.state == true do --处理FBX文件
        (
            local a = find_file 1
            if a != undefined do
            (
                for i in a do
                (
                    new_name_file i
                )
            )
        )
        if check_max.state == true do --处理MAX文件
        (
            local a = find_file 2
            if a != undefined do
            (
                for i in a do
                (
                    new_name_file i
                )
            )
        )
    )

)
rollout key_slid "动画分段标记.v1.1" width:205 height:350
(
    listbox bt_key_list "" --width:40 height:40
    button bt_do_add "添加" width:40  across:4 tooltip:"添加当前帧"--offset:[-1,-2]
    button bt_do_close "清除" width:40 tooltip:"清除选中对象的导出分段信息"
    button bt_do_w "写入" width:40 tooltip:"写入导出分段信息到对象"
    button bt_do_r "读取" width:40 tooltip:""

    listbox bt_r_key_list ""
    hyperlink bt_info "分段标记工具" address:"https://github.com/4698to/Joetime.linetool.bar/tree/master/Auto%20Export%20FBX" align:#Center

    --local set_key_num = 0
    local set_key_list = #()
    local set_key_list_box_item = #() --列表显示内容
    local set_key_list_box_item_r = #()
    local sele_Error_01 = "请选中一个对象,勿多选!\n\r "
    local split_w_text
    --local get_info_test=""
----------------------------------------------------------------------------
    fn reverse_array array =  --反转数组列表
    (   local tem_array = #()
        for i=0 to array.count do (
            if i == array.count do continue
            local tem_a = array[array.count - i]
            append tem_array tem_a
        )
        array = tem_array
    )
----------------------------------------------------------------------------
    on bt_do_add pressed do (
        key_spli = (sliderTime.frame as integer) --as string
        --set_key_num += 1
        append set_key_list key_spli --关键帧列表
        set_key_list = makeUniqueArray set_key_list --去重
        set_key_list = sort set_key_list  --重新排序
        set_key_list_box_item = #()
        for i in set_key_list do (
            append set_key_list_box_item (i as string)
        )
        bt_key_list.selection = findItem set_key_list key_spli
        bt_key_list.items = set_key_list_box_item --更新下拉列表
    )

    on bt_do_close pressed do
    (
        --set_key_num = 0
        set_key_list = #()
        set_key_list_box_item = #()
        bt_key_list.items = set_key_list_box_item
        split_w_text =""

        try
        (
            for i in selection do
            (
                setUserPropBuffer i ""
            )
            exportWindow.key_slid_name.text =""
        )catch()
        bt_r_key_list.items = set_key_list_box_item_r = #()
    )

    on bt_do_w pressed do
    (
        --set_key_num = set_key_list.count
        if set_key_list.count > 1 do
        ( -- 防止只有一帧也点了 写入按键
            if selection.count == 1 then
            (
                setUserPropBuffer selection ""--清空
                split_w_text = ""
                for i=1 to set_key_list.count do
                (
                    as_02 = i+1
                    if as_02 > set_key_list.count do continue

                    text_01 = set_key_list_box_item[i] +"#"+ set_key_list_box_item[as_02]--+"\r\n"

                    split_w_text = (i as string) + "=" + text_01+"," + "\r\n" + split_w_text

                    --setUserProp selection (i as string) text_01
                    --setUserProp <node> <key_string> <value>
                    --getUserProp <node> <key_string>
                )

                try (exportWindow.key_slid_name.text = selection[1].name)catch()

                if (setUserPropBuffer selection split_w_text) == ok do ( messageBox " 成功写入选中对象，查看请点击读取按钮 \n\r ")

            )
            else
            (
                messagebox sele_Error_01
            )--selection only one
        )
    )

    on bt_do_r pressed do (
        if selection.count ==1 then
        (
                local get_info_text = getUserPropBuffer selection[1] --读取分段信息
                set_key_list_box_item_r = filterString get_info_text "," --按","整理信息
                try (deleteItem set_key_list_box_item_r (set_key_list_box_item_r.count))catch()
                set_key_list_box_item_r = reverse_array set_key_list_box_item_r  --反转数组列表
                bt_r_key_list.items = set_key_list_box_item_r
        )
        else
        (
            messageBox sele_Error_01
        )
    )
)



rollout exportWindow "批量导出FBX v.2.2"
(
	global j_exp
	struct exp_test
	(
		copyType=1,
		exConfigFile="",
		pathSource,
		pathSave,
		set_ExportFBXPreset=#(),

		cust_file = "", -- 当前操作的文档
		export_file_name = #() ,--导出骨骼名单
		export_file_list = #(),-- 导出骨骼列表

		tem_file_fbx,--导出 FBX 集合
		tem_file_max,--导出 MAX 集合
		--set_Exp_settings = #(),
		--CopyPasteAniIni_name = (getdir #userScripts) + "\\joe_scripts\\"+ "CAT-Posture_Anim_2" + ".ini" ,
        CopyPasteAniIni_name,--导出配置文件
        key_spli=#(),--动画分段信息,string
        -------------------
        get_spli_text=#(),
        set_key_list_box_item_r,
        str_inte,

        new_str_b,
		---------------------------------------------------------------------
        fn Transform_Zero = --归零操作
        (
            if exportWindow.orange_obj_name.text != "" and exportWindow.orange_export.state do
            (
                local tem_name = exportWindow.orange_obj_name.text
                local orange_obj = execute("$"+"'"+tem_name+"'")
                if (IsValidNode orange_obj) do
                (
                    sliderTime = animationRange.start ; orange_obj.parent = undefined
                    if classof orange_obj != Biped_Object do --then CAt 骨骼这里可能会出错吧
                    (
                        animate off; orange_obj.transform = (matrix3 [1,0,0] [0,1,0] [0,0,1] [0,0,0])

                    )
                    /*
                    else
                    (
                        animate on
                        (
                            orange_obj.transform = (matrix3 [1,0,0] [0,1,0] [0,0,1] [0,0,0])
                            rotate orange_obj (angleaxis -90 [0,0,1])
                        )
                    )
                    */
                )
            )
        ),
        Fn SetKeyToInteger t dividing =--清除非整数帧
        (
            if t > dividing then
            (
                t = Ceil t.Frame
            )
            else (
                t= Floor t.Frame
            )
        ),
        --MapKeys $ SetKeyToInteger 0.5 #allKeys
        Fn CleanOutRangeKeys inputObject = --清除时间轴范围帧
        (
            startTime = AnimationRange.Start
            endTime = AnimationRange.End
            for i = 1 to inputObject.numSubs do
            (
                tempSubAnim = GetSubAnim inputObject i
                tempController = tempSubAnim.Controller

                if tempController != undefined do
                (
                    addNewKey tempController startTime;addNewKey tempController endTime --时间轴头尾加帧

                    tempKeyList = tempController.Keys

                    outEndKeysIndex = for i = 1 to tempKeyList.Count where tempKeyList[i].Time > endTime collect i
                    if outEndKeysIndex.Count > 0 do for i = 1 to outEndKeysIndex.Count do DeleteKey tempKeyList tempKeyList.count

                    outStartKeysIndex = for i = 1 to tempKeyList.Count where  tempKeyList[i].Time < startTime collect i
                    for i = 1 to outStartKeysIndex.Count do DeleteKey tempKeyList 1
                )
                if tempSubAnim.numSubs > 0 do CleanOutRangeKeys tempSubAnim
            )
            if exportWindow.check_04.state  do (MapKeys inputObject j_exp.SetKeyToInteger 0.5 #allKeys)
        ),
        --for tempObject in Objects as Array do CleanOutRangeKeys tempObject
        fn execute_string_before = --执行附加命令语句
        (
            --刚加载MAX、FBX之后
            if exportWindow.check_01.state do
            (
                try (execute exportWindow.comment_01.text) catch(print "加载时的附加语句出错！！")
            )
        ),
        fn execute_string_after = --执行附加命令语句
        (
            --导出FBX之后
            if exportWindow.check_02.state do
            (
                try (execute exportWindow.comment_02.text) catch(print "导出之后的附加语句出错！！")
            )
        ),
        fn select_object = --导出对象模式
        (
            if exportWindow.sele_mod.state == 1 then
            (
                local set_name = exportWindow.selec_set.text
                nss = selectionSets[set_name]
                if nss != undefined do
                (
                    for i in nss do (j_exp.CleanOutRangeKeys i )--
                    select nss
                )
            )
            else
            (
                j_exp.get_export_bone_filename_list() --读取导出骨骼名单
                for i in j_exp.export_file_list do (j_exp.CleanOutRangeKeys i )
                select j_exp.export_file_list --选择导出对象
            )
        ),
		fn StringIsEmpty str=
		(
			if (str==undefined or str=="" or str==" ") then
			(
				return true
			)else
			(
				return false
			)
		),
		------------------------------------------------------------------------
        fn makedir_string path_string b_string = --来源同级下的FBX 文件夹
        (
            local tem = filterString path_string "\\"
            if tem.count != 0 do
            (
                fbx_path = ""
                for i = 1 to (tem.count - 1 ) do
                (
                    fbx_path += tem[i] + "\\"
                )
                return (fbx_path + b_string )
            )

        ),
		fn chk_pathSave =
		(
			if (doesFileExist j_exp.pathSave ) == false do
			(
				makeDir j_exp.pathSave
			)
		),
		------------------------------------------------------------------------
		fn reverse_array array =  --反转数组列表
		(   local tem_array = #()
		    for i=0 to array.count do (
		        if i == array.count do continue
		        local tem_a = array[array.count - i]
		        append tem_array tem_a
		    )
		    array = tem_array
		),
		---------------------------------------------------------------------
		fn get_end_key_time =  --获取obj 头尾帧 ，用来控制导出时间轴区间
		(
            if exportWindow.chk_key_spli_02.state then
            (
                --local obj_name = getINISetting j_exp.CopyPasteAniIni_name "SaveHistory" "root_key"
                local obj_name = exportWindow.key_slid_name.text
                try (local obj = execute("$"+"'"+obj_name+"'")) catch()
                if obj != undefined then --当找到帧区间标记对象时
                (
                	 j_exp.get_spli_text = getUserPropBuffer obj--检测是否有分段动画信息
                	if j_exp.get_spli_text == "" then --没有动画分段信息时
                	(
                        return true
    	            )
    	            else--有动画分段信息时
    	            (
    		                j_exp.set_key_list_box_item_r = filterString j_exp.get_spli_text "," --按","整理信息
                            try (deleteItem j_exp.set_key_list_box_item_r (j_exp.set_key_list_box_item_r.count))catch()
                            j_exp.set_key_list_box_item_r = j_exp.reverse_array j_exp.set_key_list_box_item_r  --反转数组列表

                            bb = j_exp.set_key_list_box_item_r.count
                            j_exp.key_spli = #()
                            for ie=1 to bb do
                            (
                                j_exp.str_inte = filterString j_exp.set_key_list_box_item_r[ie] "=#\r\n"
                                append j_exp.key_spli j_exp.str_inte
                            )
                            return false --true
    	            )
                )
                else (return true ) --当没找到帧区间标记对象时，只能是按开文件时的时间轴导出
            )
            else
            (
                return true
            )
		),
		---------------------------------------------------------------------
		fn set_anim_spli_timeline key_arr =
		(
			-- 如： key_arr = #("1", "0", "41") key_arr[1]是帧标记序号; key_arr[2] 是时间轴start ;key_arr[3] 是时间轴end
			try
			(
				local s_t = key_arr[2] as Integer
				local e_t = key_arr[3] as Integer
				animationRange = interval s_t e_t
			)catch()

		),
		---------------------------------------------------------------------
		fn set_bt_get_root_key obj =  --写入导出区间标记骨骼名
		(
			setINISetting j_exp.CopyPasteAniIni_name "SaveHistory" "root_key" obj.name
		),

		fn get_bt_get_roo_key = --读取导出区间标记骨骼名
		(
			getINISetting j_exp.CopyPasteAniIni_name "SaveHistory" "root_key"
		),

		fn create_config = --创建配置文件 Export_config.ini
		(
			--if set_Exp_settings.count != 0 then (
				if j_exp.CopyPasteAniIni_name == undefined then
				(
					if j_exp.pathSource == undefined then
					(
						j_exp.CopyPasteAniIni_name = (getdir #userScripts) + "\\"+ "CAT-Posture_Anim_2" + ".ini" --在没有设置源路径 时，使用默认目录
					)
					else
					(
						j_exp.CopyPasteAniIni_name = j_exp.pathSource + "\\Export_config"+".ini" --设置源路径时，在源路径下新建
					)
					--append j_exp.set_Exp_settings j_exp.CopyPasteAniIni_name

					--j_exp.set_Exp_settings = makeUniqueArray j_exp.set_Exp_settings
					--exportWindow.ddl_expoer_Preset.items = j_exp.set_Exp_settings
					--exportWindow.ddl_expoer_Preset.tooltip = j_exp.set_Exp_settings[exportWindow.ddl_expoer_Preset.selection] --as string
				)
		 		else
		 		(

					--append j_exp.set_Exp_settings j_exp.CopyPasteAniIni_name

					j_exp.set_Exp_settings = makeUniqueArray j_exp.set_Exp_settings
					--exportWindow.ddl_expoer_Preset.items = j_exp.set_Exp_settings
					--exportWindow.ddl_expoer_Preset.tooltip = j_exp.set_Exp_settings[exportWindow.ddl_expoer_Preset.selection] --as string
				)
			--)

		),
		---------------------------------------------------------------------

		fn find_file type = 	-- 找到 源 路径 文件夹里面的FBX - max 文件，忽略次级目录
		(
			local from_path = j_exp.pathSource + @"\"
			if type == 1 do (j_exp.tem_file_fbx = getFiles (from_path + "*"+".FBX"))
			if type == 2 do (j_exp.tem_file_max = getFiles (from_path + "*"+".max"))

		),
		---------------------------------------------------------------------
		fn load_fiel fpath = --导入 MAX FBX
		(
			if (getFilenameType fpath) == ".FBX" do
            (
				FBXImporterSetParam "Mode" #create --设置导入类型 #create (Add) #exmerge (Add and Update Animation) #merge (Update animation).
				importFile fpath #noPrompt
			)
			if (getFilenameType fpath) == ".max" do
            (
				try (
					loadMAXFile fpath useFileUnits:true quiet:true  -- 打开max 文件

					)
				catch(print "版本不匹配？")
			)

		),
        fn CH_chk str = --去掉中文
        (
            if str.count != 0 do
            (
                new_str_a = filterString str "_ - . , ) (" --去掉符号
                j_exp.new_str_b = ""
                for i=1 to new_str_a.count do
                (
                    regCN = "[\u4e00-\u9fa5]"
                   -- regEN = "[a-zA-Z]"
                    a_m = (dotNetObject "System.Text.RegularExpressions.Regex" regCN).isMatch new_str_a[i] --isMatch Split
                    if a_m==false do
                    (
                        j_exp.new_str_b += (new_str_a[i]+"_")
                    )
                )

                try (j_exp.new_str_b = substring j_exp.new_str_b 1 ((j_exp.new_str_b.count)-1))catch()
                return j_exp.new_str_b
            )
        ),
		---------------------------------------------------------------------
        fn export_mod = --导出FBX 设置
        (
            if exportWindow.export_mode_anim.state == 1 then
            (
                FbxExporterSetParam "ResetExport" ;
                 FbxExporterSetParam "SmoothingGroups" true ;
                 FbxExporterSetParam "SmoothMeshExport" true
                FbxExporterSetParam "Animation"  false;
                FbxExporterSetParam "EmbedTextures" exportWindow.Embed_Textures.state
            )
            else
            (
                FbxExporterSetParam "ResetExport"
                FbxExporterSetParam "Animation"  true;
                FbxExporterSetParam "BakeAnimation"  exportWindow.bake_anim.state --false
                FbxExporterSetParam "BakeResampleAnimation"  exportWindow.resample_all.state

                FbxExporterSetParam "FilterKeyReducer"  exportWindow.Curve_Filters.state ;

                if exportWindow.Up_axis.state == 2 do (FbxExporterSetParam "UpAxis" "Z")

                FbxExporterSetParam "EmbedTextures" exportWindow.Embed_Textures.state


            )
        ),
		fn export_file fpath = --导出FBX
		(
			j_exp.chk_pathSave()
            local file_name = j_exp.CH_chk (getFilenameFile fpath)
            if file_name !="" then
			(
                local ex_file_name = j_exp.pathSave + @"\"+ file_name +".FBX"  -- 导出文件名 与当前操作文件同名
            )
            else(
                local ex_file_name = j_exp.pathSave + @"\"+ (getFilenameFile fpath) +".FBX"
            )
			--FBXExporterSetParam "LoadExportPresetFile" j_exp.exConfigFile --设置FBX导出预设(导出模型或者动画) max2015 D:\Documents\3dsMax\FBX\3dsMax2014_X64\Presets\2015.1\export
            j_exp.export_mod()
			exportFile ex_file_name #noPrompt selectedOnly:true using:#FBXEXP--theClasses--[9] --全场景导出操作，非选择导出

		),
		---------------------------------------------------------------------
		fn export_file_s fpath n =
		(
			j_exp.chk_pathSave()

            local file_name = j_exp.CH_chk (getFilenameFile fpath)
            if file_name !="" then
            (
                local ex_file_name = j_exp.pathSave + @"\"+ file_name +"_"+ (n as string ) +".FBX"  -- 导出文件名 与当前操作文件同名
            )
            else(
                local ex_file_name = j_exp.pathSave + @"\"+ (getFilenameFile fpath)+"_"+ (n as string ) +".FBX"
            )


			--FBXExporterSetParam "LoadExportPresetFile" j_exp.exConfigFile
			--local theClasses =exporterPlugin.classes
            j_exp.export_mod()
			exportFile ex_file_name #noPrompt selectedOnly:true using:#FBXEXP

		),
	--------------------------------------------------------------------- 导出骨骼
		fn set_export_bone_filename_list =  -- 写入导出骨骼名单
		(
			/*
			local all_obj = objects as array --- !!!!!!!!

			--local export_file_name = #()
			if all_obj.count != 0 do (  -- 确保场景内不为空
				for i in all_obj do(
					append export_file_name i.name
				)*/
				--CopyPasteAniIni_name = (getdir #userScripts) + "\\joe_scripts\\"+ "CAT-Posture_Anim_2" + ".ini" --配置文件
				if j_exp.export_file_name.count != 0 do
                (
					setINISetting j_exp.CopyPasteAniIni_name "obj_num" "count" (j_exp.export_file_name.count as string)	--写入配置，导出骨骼数
					for i=1 to j_exp.export_file_name.count do(
						local name_string = i as string
						local n_name = j_exp.export_file_name[i]
						setINISetting j_exp.CopyPasteAniIni_name "SaveHistory" name_string n_name --写入导出骨骼列表

                        local se_obj
                        try (se_obj = execute("$"+"'"+n_name+"'")) catch(se_obj = execute("$"+"'"+n_name+"'")) --特为Bib CAT 选择

                        if classOf se_obj == Biped_Object or classof se_obj == CATBone then --Bip CAT 骨骼导出可不勾选Bone on ，所有即使没头勾选，也都当为勾选
                        (
                        	setINISetting j_exp.CopyPasteAniIni_name "Bone_on_0_1" n_name "1"
                        )
                        else if se_obj.boneEnable then
                        (
                        	setINISetting j_exp.CopyPasteAniIni_name "Bone_on_0_1" n_name "1"
                        )--写入Bone on 开关

                        else
                        (
                        	setINISetting j_exp.CopyPasteAniIni_name "Bone_on_0_1" n_name "0"
                        )
					)
				)
		),

		---------------------------------------------------------------------
		fn get_export_bone_filename_list = --读取导出骨骼名单，bone on 值
		(
			local export_count = (getINISetting j_exp.CopyPasteAniIni_name "obj_num" "count") as integer -- 读取导出骨骼数
			--export_file_name = #()
			j_exp.export_file_list =#()

			for o=1 to export_count do (
				local bone_name = getINISetting j_exp.CopyPasteAniIni_name "SaveHistory" (o as string)
				append j_exp.export_file_name bone_name

                local g_bone_0_1 = getINISetting j_exp.CopyPasteAniIni_name "Bone_on_0_1" bone_name --读取 Bone on 值


                try (local objjj = execute("$" +"'"+bone_name+"'"))catch(local objjj = execute("$"+"'" +bone_name+"'"))

                if objjj == undefined do ( continue)

                if g_bone_0_1 == "1" then
                (
                    objjj.boneEnable = true
                )
                else
                (
                    objjj.boneEnable = false
                ) --设置 Bone on
                --if objjj == undefined do ( continue)
				append j_exp.export_file_list objjj
			)
		),
	--------------------------------------------------------------------- end 导出骨骼
		fn FindFile fPath =
		(
			--print fPath
			for dir in GetDirectories (fPath+@"\*") do
			(
				--ExportFBX dir oldPath newPath
				FindFile dir
			)
			FilesProcess fPath
		)
	)
--end struct

---------------------------------------------------------------------------------
		group "目标路径"--Source Path
		(
			editText sourceTxt "Imp:" fieldWidth:270 labelOnTop:false across:3 align:#left
			button sourceButton "..." width:20 height:25 offset:[140,-5] tooltip:"设置路径"
            button sourceButton_02 "M" width:20 height:25 offset:[50,-5] tooltip:"获取当前文件路径"
		)
		group "保存路径"--Save Path
		(
			edittext prefix_Save "Out:" fieldWidth:270 labelOnTop:false across:2 align:#left
			button btn_Save "..."  width:35 height:25  offset:[65,-5] tooltip:"设置保存FBX路径" --across:2 align:#right
		)
		button export_Button "自动批量导出"  width:200 height:30 tooltip:"执行自动导出操作"--across:2 alingn:#cent
		--checkbutton  chk_Config  "OpenConfig"  width:100 height:25
		--button chk_Config  "OpenConfig"  width:100 height:25
		group "导出对象" --Setting
		(
					--checkbox load_fiel_type_fbx "" offset:[1,0] across:4
					--label lblInfo_fbx "FBX" offset:[-95,0] tooltip:"处理FBX文件"--align:#left
                    --checkbox check_sele_set  "" across:3
                    radiobuttons sele_mod labels:#("选择集", "手动选") columns:1 align:#left across:2 offsets:#([0,0],[0,10])
                    edittext selec_set ""  fieldWidth:270 labelOnTop:false offset:[-105,0] tooltip:"填选择集名字"


                    --label lab_01 "选择集" offset:[30,0]

					--checkbox chek_sele_a  "" checked:true across:3
				    button bt_get_exp_list "当前选中 为导出对象" width:270 height:20 tooltip:"将当前选中对象设置为导出对象，会记录下对象的Bone on属性" offset:[32,-22]
                    --label lab_03 "手动选" offset:[30,0]
                    checkbox orange_export "归零"  across:2 tooltip:"填需要归零导出对象名字"
                    edittext orange_obj_name "" fieldWidth:270 labelOnTop:false offset:[-105,0]

                    progressBar Bar_a  width:338 height:16 color:red offset:[3,0]
		)
        group "附加命令"
        (
                    checkbox check_01 "" across:3
                    edittext comment_01 ""  fieldWidth:270 labelOnTop:false offset:[-95,0]
                    label lab_04 "加载时" offset:[30,0]

                    checkbox check_02 "" across:3
                    edittext comment_02 ""  fieldWidth:270 labelOnTop:false offset:[-95,0]
                    label lab_05 "导出后" offset:[30,0]

                    checkbox check_03 "清除时间轴外帧" checked:true enabled:false
                    checkbox check_04 "清除非整数帧"
        )
        group "标记分段" (
                    --button bt_get_root_key "帧区间标记" width:80 height:20  tooltip:"设置导出时间轴长度 标记对象" across:4 enabled:false--offset:[-1,-2]
                    --checkbox chk_key_spli_01 "" offset:[8,2] tooltip:"是否启用时间轴标记" enabled:false

                    checkbox chk_key_spli_02 "分段标记对象" offset:[0,2] tooltip:"是否启用分段标记" across:3 --enabled:false
                    edittext key_slid_name "" offset:[-10,2] tooltip:"填标记对象名字"
                    button bt_key_split "分段标记工具" width:80 height:20 tooltip:"" --enabled:false
        )
		group "FBX设置"--Preset
		(
		    -- Group body.

			--label exp_config "导出预设:" across:3 offset:[-30,3] enabled:false
			--dropdownlist ddl_expoer_Preset "" width:240 height:20 items:(j_exp.set_Exp_settings) tooltip:"" offset:[-50,0] enabled:false
			--button bt_config_1 "..." width:25 height:20 offset:[45,0] tooltip:"打开文件夹" enabled:false

			--label cbx_FBX_pre "FBX预设:" across:3 offset:[-30,3]
		     --dropdownlist ddlOutputpath width:240 height:20 items:(_data.optionOutputPath.Value()) tooltip:"" offset:[-40,0]
			--dropdownlist ddlPreset "" width:240 height:20 items:(j_exp.set_ExportFBXPreset) tooltip:"" offset:[-50,0] enabled:false
			--button btnGetFolder "..." width:25 height:20 tooltip:"打开文件夹" offset:[45,0] enabled:false

            radiobuttons export_mode_anim "" labels:#("模型", "动画") default:2-- 导出模式 模型和动画
            checkbox Embed_Textures "EmbedTextures" across:4
            checkbox bake_anim "BakeAnima" offset:[12,0] --checked:true
            checkbox resample_all "ReasamleAll" offset:[5,0]

            checkbox Curve_Filters "CurveFilters" checked:true
            radiobuttons Up_axis labels:#("Y-up","Z-up") columns:2

		)
        /*
        group "命名" (
            checkbox chk_ch
        )
        */
        button name_tool "批量命名工具" across:2 offset:[60,0]
		hyperlink lbl_01 "About" address:"https://github.com/4698to/Joetime.linetool.bar/tree/master/Auto%20Export%20FBX" offset:[30,5]--align:#Center

		--button btn_ExConfigPath "Find Export Configuration File " width:355 \
		--tooltip:"EX: C:\Users\UserName\Documents\3dsMax\FBX\3dsMax2014_X64\Presets\2015.0\export"
---------------------------------------------------------------------------------
        on name_tool pressed do
        (
            createDialog rename_File
        )
		on bt_key_split pressed do (
			createDialog key_slid
		)
		--on load_fiel_type_fbx changed state do (type_fbx = state ) --设置处理 FBX 文档类型
		--on load_fiel_type_max changed state do (type_max = state ) --设置处理 MAX 文档类型 可同勾选两项
        /*
		on ddl_expoer_Preset selected itm do
		(
			j_exp.CopyPasteAniIni_name = exportWindow.ddl_expoer_Preset.items[itm]
			exportWindow.ddl_expoer_Preset.tooltip = j_exp.set_Exp_settings[itm] --as string
		)

		on bt_config_1 pressed do  --设置导出对象预设
		(
			local g_conig_path = j_exp.pathSave
			if j_exp.pathSave == undefined do
            (
				g_conig_path = ((getdir #userScripts) + "\\joe_scripts\\")
			)
			local get_Export_obj_config= getOpenFileName  types:"ini(*.ini)|*.*" filename: g_conig_path--j_exp.pathSave--((getdir #userScripts) + "\\joe_scripts\\") --优先路径

			if get_Export_obj_config != undefined do(

				j_exp.CopyPasteAniIni_name = get_Export_obj_config

				append j_exp.set_Exp_settings get_Export_obj_config
				j_exp.set_Exp_settings = makeUniqueArray j_exp.set_Exp_settings

				--更新 UI
				exportWindow.ddl_expoer_Preset.items = j_exp.set_Exp_settings
				--exportWindow.ddl_expoer_Preset.tooltip = set_Exp_settings[exportWindow.ddl_expoer_Preset.selection]--as string

				exportWindow.ddl_expoer_Preset.selection = findItem j_exp.set_Exp_settings j_exp.CopyPasteAniIni_name
				ddl_expoer_Preset.tooltip = j_exp.CopyPasteAniIni_name

                --bt_get_root_key.text = j_exp.get_bt_get_roo_key()
				bt_get_exp_list.text = getINISetting j_exp.CopyPasteAniIni_name "obj_num" "count"
			)
		)

		on bt_get_root_key pressed do -- 选取导出时间轴区间标记对象
		(
			if selection.count != 0 then (

				j_exp.create_config()
				j_exp.set_bt_get_root_key selection[1]
				bt_get_root_key.text = selection[1].name
				)
			else (
				messagebox("请先选中 标记对象 \n\r .")
				)
		)
        */
		---------------------------------------------------------
		on bt_get_exp_list pressed do --选取导出对象
		(
			if selection.count != 0 then (
				j_exp.export_file_name =#()
				for i in selection do(
					append j_exp.export_file_name i.name
				)
				bt_get_exp_list.text = (j_exp.export_file_name.count as string) + " 个导出对象"
				j_exp.create_config() --创建
				j_exp.set_export_bone_filename_list() --写入
			)
			else (
				messagebox("请先选中 导出对象 \n\r .")
				)
		)
		on sourceTxt changed txt do
			(
				--And the name is not the empty string,
				if txt != "" do
				(
					pathSource = txt
				)

			)


		on sourceButton pressed do
			(
				local sp = getSavePath caption "Select Source Path"
				if sp!=undefined do
				(
					sourceTxt.text= sp
					j_exp.pathSource=sp
					j_exp.pathSave = j_exp.pathSource + "\FBX"
					prefix_Save.text = j_exp.pathSave
				)

			)
        on sourceButton_02 pressed do
            (
                --local sp = getSavePath caption "Select Source Path"
                local sp = maxfilepath --使用当前文件路径
                if sp != "" do
                (
                    sourceTxt.text = sp
                    j_exp.pathSource = sp
                    --j_exp.pathSave = j_exp.pathSource + "\FBX"
                    j_exp.pathSave = j_exp.makedir_string sp "FBX"
                    prefix_Save.text = j_exp.pathSave
                )

            )

		on prefix_Save changed txt do
			(
				--And the name is not the empty string,
				if txt != "" do
				(
					j_exp.pathSave=txt
				)
			)

		on btn_Save pressed do
		(
			local sp_2= getSavePath caption "Select Save Path"
			if sp_2!=undefined do
			(
				prefix_Save.text= sp_2
				j_exp.pathSave=sp_2
			)
		)




		on export_Button pressed do
		(
				--print sourceTxt.text
				--print saveTxt.text

				if (j_exp.StringIsEmpty j_exp.pathSource) then
				(
					messagebox("请设置源路径 \n\r ")
				)
                /*
				else if (j_exp.StringIsEmpty j_exp.exConfigFile)then
				(
					messagebox(" 请设置FBX导出预设 .\n Example C:\Users\UserName\Documents\
						\n 3dsMax\FBX\3dsMax2014_X64\Presets\2015.0\export")
				)
                */
				else
				(
					--try
					--(
						j_exp.find_file 2
						if j_exp.tem_file_max.count != 0 do
						(
							for i=1 to j_exp.tem_file_max.count do
							(
								j_exp.load_fiel j_exp.tem_file_max[i] --打开导入MAX-FBX

                                j_exp.execute_string_before() --执行附加语句

								j_exp.cust_file = j_exp.tem_file_max[i]

	                            if j_exp.get_end_key_time() then --设置导出时间轴 并 检测分段信息 ,如果 检测到有动画分段信息返回:false  没有检测到返回 true
	                            (
									--j_exp.get_export_bone_filename_list() --读取导出骨骼名单
									--select j_exp.export_file_list --选择导出对象
                                    j_exp.Transform_Zero() -- 归零操作
                                    j_exp.select_object()  --选择导出对象
									j_exp.export_file j_exp.tem_file_max[i] --导出
								)
	                            else
	                            (
	                            	for p=1 to j_exp.key_spli.count do
	                            	(
                                        j_exp.load_fiel j_exp.cust_file -- 分段导出需要多次加载文件
	                            		j_exp.set_anim_spli_timeline j_exp.key_spli[p] -- 设置导出时间轴
                                        j_exp.Transform_Zero()-- 归零操作
                                        --j_exp.get_export_bone_filename_list()
	                            		--select j_exp.export_file_list
                                        j_exp.select_object()  --选择导出对象
	                            		j_exp.export_file_s j_exp.tem_file_max[i] p
	                            	)
	                            )

                                j_exp.execute_string_after()--执行附加语句

                                Bar_a.value = 100.*i/(j_exp.tem_file_max.count)
							)
                            Bar_a.value = 0
						)
					--)
					--catch
					--(
						--format "*** % ***\n" (getCurrentException())
					--)
				)
		)

		/*
		on chk_Config changed state do
		(
				if state then
				(
					exportWindow.height=350
				)
				else
				(
					exportWindow.height=135
				)
		)

		on chk_Config pressed do
		(

		)

		on btn_ExConfigPath pressed do
		(
			f = getOpenFileName types:"Data(*.fbxexportpreset)|*.fbxexportpreset"
			if f!=undefined do
			(
				btn_ExConfigPath.text=f
				exConfigFile=btn_ExConfigPath.text
			)
		)*/

		--SubRollout theSubrollout "Configuration" height:95  --width:360 offset:[-5,0]

		on ddlPreset selected itm do
		(
			ddlPreset.tooltip = filenamefrompath (ddlPreset.items[itm] as string)
			j_exp.exConfigFile=ddlPreset.items[itm]
		)

		on btnGetFolder pressed do
		(
			local get_ExportFBXPreset = getOpenFileName filename:"D:\Documents\3dsMax\FBX\3dsMax2014_X64\Presets\2015.1\export\\" types:"Data(*.fbxexportpreset)|*.fbxexportpreset"
			if get_ExportFBXPreset != undefined do
            (
				append j_exp.set_ExportFBXPreset get_ExportFBXPreset
				j_exp.exConfigFile = get_ExportFBXPreset
				ddlPreset.items = j_exp.set_ExportFBXPreset
				ddlPreset.selection = findItem j_exp.set_ExportFBXPreset j_exp.exConfigFile
				ddlPreset.tooltip = filenamefrompath (j_exp.exConfigFile as string)
				--exConfigFile=ddlPreset.items[itm]
			)
			/*
			if f!=undefined do
			(
				btn_ExConfigPath.text=f
				exConfigFile=btn_ExConfigPath.text
			)
			*/
		)
)
j_exp = exportWindow.exp_test()
createDialog exportWindow 370 530--135
	--AddSubRollout exportWindow.theSubrollout exportConfig


