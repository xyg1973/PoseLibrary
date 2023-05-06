from pymxs import runtime as rt


selectionobjs = rt.selection
objs = []
if selectionobjs!=None:
	for i in range(selectionobjs.count):
		objs.append(selectionobjs[i].name)

textobjs = str(objs)
objsname = eval(textobjs)
print(objsname)
