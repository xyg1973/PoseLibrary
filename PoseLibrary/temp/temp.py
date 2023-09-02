import json

path = "F:/Myself/SN_Game/folder_7/pose.json"

textA = [{u'type': u'Pose'}, {u'objscale': u'[1,1,1]', u'obj': u'$Box:Box001 @ [25.174984,7.694165,-23.788651]', u'objposition': u'[25.175,7.69417,-23.7887]', u'objparent': None, u'objname': u'Box001', u'objtype': u'Box', u'objrotation': u'(quat -0.361834 0.00447465 0.0176429 0.932065)', u'objtransform': u'(matrix3 [0.999337,0.0296506,-0.021109] [-0.0361269,0.737529,-0.674348] [-0.00442633,0.674664,0.738112] [25.175,7.69417,-23.7887])'}]
# with open(path) as file:
#     # 使用 readlines() 读取所有行并储存在列表中
#     lines = file.readlines()
#     # 获取第2行（索引从0开始，因此需要使用索引1来获取第2行）
#     type_text = lines[1].strip()+lines[2].strip()+lines[3].strip()
#
#
# type_text = type_text[:-1]
# type_text = eval(type_text)
# file_type = type_text.get("type")
# print(file_type)
with open(path, 'r') as file:
    posedata = json.load(file)


data = posedata.pop(-1)
print(data)
print(textA[1].get("objname"))
