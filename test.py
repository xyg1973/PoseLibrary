import win32com.client

MaxApp = "MAX.Application"
script = "clearlistener(); for i = 1 to 100 do print i"
max_functions = ["OLEExecuteScript","runscript"]

conn = win32com.client.Dispatch(MaxApp)
for funcs in max_functions: # add our OLE functions
	conn._FlagAsMethod(funcs)

conn.runscript(script)