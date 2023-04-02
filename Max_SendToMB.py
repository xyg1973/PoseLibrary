import pymxs
from pymxs import runtime as rt
import MaxPlus
# macroscript_name = 'My_Macroscript'
# macroscript_category = 'Test'
# menu = rt.menuMan.createMenu("MyMenu")
# help_menu = rt.menuMan.findMenu('&Help')
# print(help_menu)
# item = rt.menuMan.createActionItem("MyAction", "print \"Hello World!\"")
# help_menu.addItem(item, -1)
# rt.menuMan.updateMenuBar()
# # print(MaxPlus.Menu.GetItem())
# # rt.menuMan.addItem(menu, item)


macroScript UpdateScene category:"SN_AnimTool" --some macro script
(
	print "I do nothing, but I am on a Menu!"
)

theMainMenu = menuMan.getMainMenuBar() --get the main menu bar
theMenu = menuMan.createMenu "SN_AnimTool" --create a menu called Forum Help
theSubMenu = menuMan.createSubMenuItem "SN_AnimTool" theMenu --create a SubMenuItem
theMainMenu.addItem theSubMenu (theMainMenu.numItems()+1) --add the SubMenu to the Main Menu
theAction = menuMan.createActionItem "UpdateScene" "SN_AnimTool" --create an ActionItem from the MacroScript
theMenu.addItem theAction (theMenu.numItems()+1) --add the ActionItem to the menu
menuMan.updateMenuBar() --update the menu bar