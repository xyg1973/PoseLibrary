from pymxs import runtime as rt
import pymxs


def ls():
    allobj = []
    objs = rt.selection
    for obj in objs:
        allobj.append(obj)
    return allobj


b = ls()[0]
# print(b.numsubs)
for i in range(b.numsubs):
    sub = rt.getSubAnim(b, i + 1)
    # print(f'{sub.name} [{sub_i+1}]')

    if sub.controller == None:

        print(' No controller assigned to it')
    else:

        print("current controller: {}".format(sub.controller))
        if sub.keys == None:
            print("No keys assigned to it")

    for secsub_i in range(sub.numsubs):

        secsub = mxs.getSubAnim(sub, secsub_i + 1)
        print('{} [{}]'.format(secsub.name, (secsub_i + 1))

              # if secsub.controller == None:
              # print(' No controller assigned to it')
              # else:
              # pass
              # print(f'\t current controller: {(secsub.controller)}')
              # if secsub.keys == None:
              # pass
              # print('\t No keys assigned to it')
            for thirdsub_i in range(secsub.numsubs):
                thirdsub = mxs.getSubAnim(secsub, thirdsub_i + 1)
                # print(f'\t\t{thirdsub.name} [{thirdsub_i+1}]')
                if secsub.controller == None:
                    pass
                # print('\t No controller assigned to it')
                else:
                    pass
        # print(f'\t\t current controller: {(thirdsub.controller)}')

        xkeytimelist = []
        obj_ctrl = mxs.getPropertyController(obj.controller, 'Position')
        obj_ctrl_posx = mxs.getPropertyController(obj_ctrl, 'X Position')

        print(mxs.numkeys(obj_ctrl_posx))

        # for i in range(rt.numkeys(obj_ctrl_posx)):
        #	if obj_ctrl_posx.keys[i].isKeySelected ==True:
        #		timenums = i.getKeyTime
        #		xkeytimelist.append(timenums)

        # a = rt.trackviews.current
        # print(rt.trackviews.current.expandTracks())
        # print(obj.numSubs)
        # print(rt.getSubAnimName(obj,3,asString=True,localizedName=True))
        # print(rt.getSubAnim(obj,5))
        # rt.position.controller.x
        # print(obj(3,SubAnim="Transform"))
        # b = rt.box()
        # b[4].object

