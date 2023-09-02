import sys
import os

current_work_dir = os.path.dirname(__file__)
# poselibrary_path = current_work_dir

if current_work_dir in sys.path:
    pass
else:
    sys.path.append(current_work_dir)

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


def run():
    pypath = os.getcwd()
    pypath = pypath+"\python"


    from PoseLibrary.UI import windowUI as windowUI
    from PoseLibrary.Tools import file as file
    try:
        reload_module('PoseLibrary.UI.windowUI')
        reload_module('PoseLibrary.Tools.file')
    except:
        pass
    #
    my_documents_path = os.path.expanduser('~/Documents')
    file_path = file.check_and_create_file(my_documents_path, 'poselibrary', 'poselibrary.txt')
    windowUI.pypath = pypath + "\PoseLibrary"
    window = windowUI.main()

if __name__ == "__main__":
    run()