def reload_module(module_name):
    if module_name in sys.modules:
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
my_documents_path = os.path.expanduser('~/Documents')
file_path = file.check_and_create_file(my_documents_path, 'poselibrary', 'poselibrary.txt')
windowUI.pypath = pypath + "\PoseLibrary"
window = windowUI.main()