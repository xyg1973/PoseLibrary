rollout AlignBoneAnimation "Align Animation" width:280 height:336
(
	pickButton 'btn_pick_reference' "Reference" pos:[142,23] width:120 height:28 align:#left
	pickButton 'btn_pick_target' "Target" pos:[14,23] width:120 height:28 align:#left
	groupBox 'grp1' "local position" pos:[14,69] width:247 height:48 align:#left
	groupBox 'grp2' "local rotation" pos:[15,137] width:245 height:51 align:#left
	checkbox 'chk_pos_x' "x" pos:[38,91] width:31 height:12 align:#left
	checkbox 'chk_pos_y' "y" pos:[123,91] width:31 height:12 align:#left
	checkbox 'chk_pos_z' "z" pos:[203,91] width:31 height:12 align:#left
	checkbox 'chk_rotate_x' "x" pos:[38,160] width:31 height:12 align:#left
	checkbox 'chk_rotate_y' "y" pos:[124,160] width:31 height:12 align:#left
	checkbox 'chk_rotate_z' "z" pos:[204,160] width:31 height:12 align:#left
	button 'btn_align' "Align" pos:[15,283] width:245 height:26 align:#left
	groupBox 'grp5' "local scale" pos:[15,207] width:245 height:51 align:#left
	checkbox 'chk_scale_x' "x" pos:[38,230] width:31 height:12 align:#left
	checkbox 'chk_scale_y' "y" pos:[124,230] width:31 height:12 align:#left
	checkbox 'chk_scale_z' "z" pos:[204,230] width:31 height:12 align:#left
	
	local targetBone
	local refBone
	local chk_pos_x_state=false
	local chk_pos_y_state=false
	local chk_pos_z_state=false
	local chk_rotate_x_state=false
	local chk_rotate_y_state=false
	local chk_rotate_z_state=false
	local chk_scale_x_state=false
	local chk_scale_y_state=false
	local chk_scale_z_state=false
	
	on btn_pick_reference picked obj do
	(
		refBone=obj
		btn_pick_reference.text=refBone.name
	)
	on btn_pick_target picked obj do
	(
		targetBone=obj
		btn_pick_target.text=targetBone.name
	)
	on chk_pos_x changed state do
	(
		chk_pos_x_state=state
	)
	on chk_pos_y changed state do
	(
		chk_pos_y_state=state
	)
	on chk_pos_z changed state do
	(
		chk_pos_z_state=state
	)
	on chk_rotate_x changed state do
	(
		chk_rotate_x_state=state
	)
	on chk_rotate_y changed state do
	(
		chk_rotate_y_state=state
	)
	on chk_rotate_z changed state do
	(
		chk_rotate_z_state=state
	)
	on chk_scale_x changed state do
	(
		chk_scale_x_state=state
	)
	on chk_scale_y changed state do
	(
		chk_scale_y_state=state
	)
	on chk_scale_z changed state do
	(
		chk_scale_z_state=state
	)
	on btn_align pressed  do
	(
		ref_ctrl = refBone.controller
		_bone = BoneSys.createBone[0,0,0] [0,1,0] [0,0,1]
		_bone.name="temp_bake_bone"
		_bone.width =1
		_bone.height = 1
		_bone.transform = targetBone.transform
		
		posCtrl =Position_Constraint()
		_bone.pos.controller = posCtrl
		posConstraintInterface = posCtrl.constraints
		posConstraintInterface.appendTarget refBone 100
		
		rotCtrl =Orientation_Constraint()
		_bone.rotation.controller = rotCtrl
		rotConstraintInterface = rotCtrl.constraints
		rotConstraintInterface.appendTarget refBone 100
		_bone.rotation.controller.relative = on
			
		targetBone.pos.controller = Position_XYZ ()
		targetBone.rotation.controller = Euler_XYZ ()
		targetBone.scale.controller=ScaleXYZ()
		
		temp_pos_x=targetBone.pos.x as string
		temp_pos_y=targetBone.pos.y as string
		temp_pos_z=targetBone.pos.z as string
		
		temp_eular=targetBone.rotation as eulerAngles
		temp_rot_x=temp_eular.x as string
		temp_rot_y=temp_eular.y as string
		temp_rot_z=temp_eular.z as string
		
		temp_scale_x=targetBone.scale.x as string
		temp_scale_y=targetBone.scale.y as string
		temp_scale_z=targetBone.scale.z as string
		
		if chk_pos_x_state==false do 
		(
			targetBone.pos.controller.X_Position.controller = Float_Expression ()
			targetBone.pos.controller.X_Position.controller.setExpression temp_pos_x
		)
		if chk_pos_y_state==false do
		(
			targetBone.pos.controller.Y_Position.controller = Float_Expression ()
			targetBone.pos.controller.Y_Position.controller.setExpression temp_pos_y
		)
		if chk_pos_z_state==false do
		(
			targetBone.pos.controller.Z_Position.controller = Float_Expression ()
			targetBone.pos.controller.Z_Position.controller.setExpression temp_pos_z
		)
				
		if chk_rotate_x_state==false do
		(
			targetBone.rotation.controller.X_Rotation.controller = Float_Expression ()
			targetBone.rotation.controller.X_Rotation.controller.setExpression "0"
		)
		if chk_rotate_y_state==false do
		(
			targetBone.rotation.controller.Y_Rotation.controller = Float_Expression ()
			targetBone.rotation.controller.Y_Rotation.controller.setExpression "0"
		)
		if chk_rotate_z_state==false do
		(
			targetBone.rotation.controller.Z_Rotation.controller = Float_Expression ()
			targetBone.rotation.controller.Z_Rotation.controller.setExpression "0"
		)
			
		if chk_scale_x_state==false do
		(
			targetBone.scale.controller.x_scale.controller = Float_Expression ()
			targetBone.scale.controller.x_scale.controller.setExpression temp_scale_x
		)
		if chk_scale_y_state==false do
		(
			targetBone.scale.controller.y_scale.controller = Float_Expression ()
			targetBone.scale.controller.y_scale.controller.setExpression temp_scale_y
		)
		if chk_scale_z_state==false do
		(
			targetBone.scale.controller.z_scale.controller = Float_Expression ()
			targetBone.scale.controller.z_scale.controller.setExpression temp_scale_z
		)
			
		startFrame = int(animationRange.start)
		endFrame = int(animationRange.end)
		
		set animate on
		for i in startFrame to endFrame do
		(
			sliderTime = i
			targetBone.transform = _bone.transform

		)
		delete _bone
	)
)
createdialog AlignBoneAnimation