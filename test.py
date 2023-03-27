from pymxs import runtime as rt
import pymxs


def ls():
    allobj = []
    objs = rt.selection
    for obj in objs:
        allobj.append(obj)
    return allobj


def get_TrackView_SelectKeys(obj):
    allselectkeys = []
    for i in range(obj.numsubs):
        sub = rt.getSubAnim(b, i + 1)
        # print(f'{sub.name} [{sub_i+1}]')

        if sub.controller == None:
            pass
            # print(i+1)
            # print(' No controller assigned to it')
        else:
            # print(i+1)
            # print("current controller: {}".format(sub.controller))
            if sub.keys == None:
                pass
                # print("No keys assigned to it")
            for secsub_i in range(sub.numsubs):
                secsub = rt.getSubAnim(sub, secsub_i + 1)
                # print(secsub)
                if secsub.controller == None:
                    pass
                    # print('\t No controller assigned to it')
                else:
                    pass
                    # print('\t current controller: {}'.format(secsub.controller))
                if secsub.keys == None:
                    pass
                    # print('\t No keys assigned to it')
                for thirdsub_i in range(secsub.numsubs):
                    thirdsub = mxs.getSubAnim(secsub, thirdsub_i + 1)
                    # print('\t\t{} [{}]'.format(thirdsub.name, thirdsub_i + 1))
                    if secsub.controller == None:
                        pass
                        # print('\t No controller assigned to it')
                    else:
                        keydirt = {}
                        keydirt["controller"] = thirdsub.controller

                        # print('\t\t current controller: {}'.format(thirdsub.controller))
                        # print(rt.numSelKeys(thirdsub.controller))
                        selkeys = []
                        for numkeys in range(rt.numKeys(thirdsub.controller)):
                            # print(thirdsub.controller.keys)
                            # print(numkeys)
                            if rt.isKeySelected(thirdsub.controller,numkeys+1):
                                selkey = rt.getKey(thirdsub.controller,numkeys+1)
                                selkeys.append(selkey)
                        keydirt["selkeys"] = selkeys
                        # print(keydirt)
                        allselectkeys.append(keydirt)
    return allselectkeys


obj = ls()[0]
print(get_TrackView_SelectKeys(obj))



