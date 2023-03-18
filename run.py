import os
import sys
import json
import threading
import pymxs


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


import os
import sys



pypath = os.getcwd()
pypath = pypath+"\python"


from PoseLibrary.UI import windowUI as windowUI
from PoseLibrary.Tools import file as file

reload_module('PoseLibrary.UI.windowUI')
reload_module('PoseLibrary.Tools.file')
#
#文档创建配置文件
my_documents_path = os.path.expanduser('~/Documents')
file_path = file.check_and_create_file(my_documents_path, 'poselibrary', 'poselibrary.txt')
windowUI.pypath = pypath
window = windowUI.main()