import pymxs
rt = pymxs.runtime


def propSpace(propobj, Pspace=0, Rspace=0):
    objkeys = propobj.controller.keys
    count = 1
    rt.disableSceneRedraw()
    with pymxs.undo(True):
        for key in objkeys:
            propkey = rt.biped.getKey(propobj.controller, count)
            # selkey = rt.biped.getKey(secsub.controller)
            if propkey.selected == True:
                with pymxs.animate(True):
                    rt.sliderTime = propkey.time
                    objstransform = propobj.transform
                    with pymxs.attime(propkey.time):
                        propkey.posSpace = Pspace
                        propkey.rotSpace = Rspace
                        propobj.transform = objstransform

            else:
                pass
            count += 1

    rt.enableSceneRedraw()


# rt.redrawViews()
objs = rt.getNodeByName('Bip001 Prop1')
propSpace(objs, Pspace=3, Rspace=3)