import os
import sys
import json
pypath = "J:\work\Git\PoseLibrary"
# pypath = "F:\Myself\PoseLibrary"
if pypath in sys.path:
    pass
else:
    sys.path.append(pypath)


from UI import windowUI
from Tools import file as file
def reload_module(module_name):
    # 检查模块是否已经导入
    if module_name in sys.modules:
        # 如果已经导入，则重新加载
        try:
            # Python 2
            reload(sys.modules[module_name])
        except NameError:
            # Python 3
            import importlib
            importlib.reload(sys.modules[module_name])
    else:
        pass
#
reload_module('UI.windowUI')
reload_module('Tools.file')






#文档创建配置文件
my_documents_path = os.path.expanduser('~/Documents')
file_path = file.check_and_create_file(my_documents_path, 'poselibrary', 'poselibrary.txt')



ProjectPath = "F:\Myself\cache\Project_text"
project = file.AddProject(ProjectPath)
file.write_data_to_file(file_path,project)  #写入项目路径数据
common = file.read_file(file_path)

print(common)

#读取文件数据

#设置项目路径
windowUI.pypath = pypath
windowUI.PROJECT_PATH = project.get("ProjectPath")
windowUI.PROJECT_NAME = project.get("ProjectName")
# window = windowUI.test()
window = windowUI.main()

print("test")



