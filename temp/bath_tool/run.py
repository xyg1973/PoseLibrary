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


from PoseLibrary.temp.bath_tool import WindowUI

try:
    reload_module('PoseLibrary.temp.bath_tool.WindowUI')
except:
    pass

window = WindowUI.main()

