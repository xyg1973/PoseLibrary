# -*- coding: utf-8 -*-
import os

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


    # 获取路径下的png文件列表
    allfile = os.listdir(path)                     #获取item的路径下的文件和文件夹                               #定义变量存储.json文件
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