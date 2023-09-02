def reload_module(module_name):
    if module_name in sys.modules:
        try:
            # Python 2
            reload(sys.modules[module_name])
        except NameError:
            # Python 3
            import importlib
            importlib.reload(sys.modules[module_name])
        except Exception as e:
            print(e)


import os
import sys


def run():
    pypath = os.getcwd()
    pypath = pypath+"\python"


    from SN_AnimTool.tools.PoseLibrary.UI import windowUI as windowUI
    from SN_AnimTool.tools.PoseLibrary.Tools import file as file
    try:
        reload_module('SN_AnimTool.tools.PoseLibrary.UI.windowUI')
        reload_module('SN_AnimTool.tools.PoseLibrary.Tools.file')
    except:
        pass
    #
    my_documents_path = os.path.expanduser('~/Documents')
    file_path = file.check_and_create_file(my_documents_path, 'poselibrary', 'poselibrary.txt')
    windowUI.pypath = pypath + "\PoseLibrary"
    window = windowUI.main()

if __name__ == "__main__":
    run()