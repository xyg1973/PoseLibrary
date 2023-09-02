#保存cpy文件
from pymxs import  runtime as rt


def creat_BipPosture(objs,cpy_coll):
    for obj in objs:
        listObjs = []
        listObjs.append(obj)
        bipposture = rt.biped.copyBipPosture(obj.controller,cpy_coll,listObjs,rt.name("snapNone"))
        # print (rt.classOf(bipposture))
        # print(bipposture.)

def creat_BipPose(obj,cpy_coll):
    bipposture = rt.biped.copyBipPose(obj.controller,cpy_coll,rt.name("snapNone"))
    return bipposture
bip_objs = rt.selection
#创建copy collections
cpy_index = rt.biped.numCopyCollections(bip_objs[0].controller)
cpy_coll = rt.biped.createCopyCollection(bip_objs[0].controller ,"tset")
creat_BipPose(bip_objs[0],cpy_coll)
#保存copy collections
cpy_file_path = "D:\\MyCopy.cpy"
cpy_file = rt.biped.saveCopyPasteFile(bip_objs[0].controller,cpy_file_path)
#删除copy collections
rt.biped.deleteCopy(bip_objs[0].controller,rt.name("pose"),"test")
rt.biped.deleteCopyCollection(bip_objs[0].controller,cpy_index+1)
# creat_BipPosture(bip_objs,cpy_coll)
# res = rt.stringStream('')
# rt.apropos("biped",to = res)
# print(res)



a= "记录pose,获取选中的obj,判断之前是否有关键帧，如果有则记录位置，如果没有就跳过，"
