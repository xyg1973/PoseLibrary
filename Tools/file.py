# -*- coding: utf-8 -*-
import os
import json
#获取文件夹
def getforce(path):
    """

    :param path: 文件夹路径
    :return: force list 文件夹列表
    """
    force_list = []  # 所有文件夹路径
    dir_list = []  # 所有文件夹名字
    for root, dirs, files in os.walk(path):
        force_list.append(root)
        for dir in dirs:
            dir_list.append(dir)
    del force_list[0]
    return force_list


def getforceName(path):
    """
    获取路径下的文件夹，返回列表
    :param path: 所有文件夹名称
    :return: forceName 文件夹列表
    """
    force_list = []  # 所有文件夹路径
    dir_list = []  # 所有文件夹名字
    for root, dirs, files in os.walk(path):
        force_list.append(root)
        for dir in dirs:
            dir_list.append(dir)
    del force_list[0]

    return dir_list

def getfile(path,filetype):
    """
    给定路径和文件类型，返回路径下类型所有文件的路径
    :param path:
    :param flietype:
    :return: typefile path
    """
    path=path
    filetype = filetype
    filelist = []
    #处理打开library窗口没有刷新文件的问题
    if path == None:
        return filelist

    print(path)
    # 获取路径下的png文件列表
    allfile = os.listdir(path)                    #获取item的路径下的文件和文件夹                               #定义变量存储.json文件
    for i in allfile :
        if i.rfind(filetype)!=-1:         #字符串从右边开始查找包含“.json”的文件，如果没有找到返回-1，如果不等于-1表示这个文件是json文件
            filelist.append(path+"/"+i)
        else:
            pass
    return filelist

def getfileName(path):
    """

    :param path:
    :return: filename
    """
    (file,ext) = os.path.splitext(path)
    (pathA,filename) = os.path.split(path)
    count = len(filename)-len(ext)
    filename = filename[0:count]
    return filename
#获取文件命名


def read_file(file_path):
    """

    :param file_path:
    :return:
    """
    common = None

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 如果文件存在，则读取其内容并将其存储在变量common中
        with open(file_path, 'r') as f:
            common = f.read()

    return common


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


def write_data_to_file(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)


def create_folder(path):
    # 如果路径不存在，则直接创建目录
    if not os.path.exists(path):
        os.makedirs(path)
        return path
    else:
        # 如果路径存在，则在后面加上数字
        i = 1
        while True:
            new_path = path + "_" + str(i)
            # 如果新路径不存在，则创建目录并返回
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                return new_path
            else:
                # 如果新路径存在，则递增数字并继续循环
                i += 1