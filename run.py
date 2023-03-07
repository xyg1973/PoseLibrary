
import os
import sys
import json
pypath = os.getcwd()
pypath = "H:\pycharm_max_work\poselibray"
if pypath in sys.path:
    pass
else:
    sys.path.append(pypath)


from UI import windowUI

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

reload_module('UI.windowUI')

def check_and_create_file(folder_path, folder_name, file_name):
    # 构建文件夹和文件的完整路径
    poselibrary_path = os.path.join(folder_path, folder_name)
    text_file_path = os.path.join(poselibrary_path, file_name)

    # 检查文件夹是否存在
    if not os.path.exists(poselibrary_path):
        # 如果文件夹不存在，则创建它
        os.makedirs(poselibrary_path)
        # 在文件夹中创建一个空文件
        open(text_file_path, 'w').close()
    else:
        # 如果文件夹存在，则检查文件是否存在
        if not os.path.exists(text_file_path):
            # 如果文件不存在，则创建它
            open(text_file_path, 'w').close()

    # 返回文件的完整路径
    return text_file_path


def read_file(file_path):
    common = None

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 如果文件存在，则读取其内容并将其存储在变量common中
        with open(file_path, 'r') as f:
            common = f.read()

    return common


def AddProject(folder_path):
    """

    :param folder_path:
    :return: ProjectPath,ProjectName,ProjectName,
    """
    # 获取文件夹名称
    folder_name = os.path.basename(folder_path)
    {folder_path: folder_name }
    # 返回包含文件夹名称和完整路径的字典
    return {"ProjectPath": folder_path,
            "ProjectName": folder_name,
            "IsCurrent": True
            }


def write_dict_to_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)



#文档创建配置文件
my_documents_path = os.path.expanduser('~/Documents')
file_path = check_and_create_file(my_documents_path, 'poselibrary', 'poselibrary.txt')
common = read_file(file_path)

#指定项目路径
ProjectPath = "H:\pycharm_maya_work\Design"
project = AddProject(ProjectPath)
print(project )
write_dict_to_file(file_path,project)  #写入项目路径数据


#读取文件数据

#设置项目路径
windowUI.PROJECT_PATH = project.get("ProjectPath")
windowUI.PROJECT_NAME = project.get("ProjectName")
# window = windowUI.test()
window = windowUI.main()



print("tsts")
print("github")