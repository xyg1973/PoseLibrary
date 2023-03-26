from pyfbsdk import *
import math

scene = FBSystem().Scene
currentTake = FBSystem().CurrentTake

startTime = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
endTime = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()



[{'endtime': 175.0, 'starttime': 46.0, 'currenttime': 46.0},
 [
     {'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [312.722595,-104.430916,0.000000]', 'objposition': '[312.723,-104.431,0]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [312.723,-104.431,0])'}
 ],
 [
     {'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [312.611206,-104.421967,-0.311459]', 'objposition': '[312.611,-104.422,-0.311459]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [312.611,-104.422,-0.311459])'}
 ],
 [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [312.270691,-104.395363,-1.211703]', 'objposition': '[312.271,-104.395,-1.2117]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [312.271,-104.395,-1.2117])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [311.691559,-104.351456,-2.649534]', 'objposition': '[311.692,-104.351,-2.64953]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [311.692,-104.351,-2.64953])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [310.864258,-104.290596,-4.573752]', 'objposition': '[310.864,-104.291,-4.57375]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [310.864,-104.291,-4.57375])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [309.779236,-104.213158,-6.933162]', 'objposition': '[309.779,-104.213,-6.93316]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [309.779,-104.213,-6.93316])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [308.427032,-104.119484,-9.676560]', 'objposition': '[308.427,-104.119,-9.67656]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [308.427,-104.119,-9.67656])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [306.798065,-104.009926,-12.752753]', 'objposition': '[306.798,-104.01,-12.7528]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [306.798,-104.01,-12.7528])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [304.882843,-103.884857,-16.110537]', 'objposition': '[304.883,-103.885,-16.1105]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [304.883,-103.885,-16.1105])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [302.671844,-103.744621,-19.698715]', 'objposition': '[302.672,-103.745,-19.6987]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [302.672,-103.745,-19.6987])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [300.155548,-103.589577,-23.466091]', 'objposition': '[300.156,-103.59,-23.4661]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [300.156,-103.59,-23.4661])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [297.324432,-103.420090,-27.361465]', 'objposition': '[297.324,-103.42,-27.3615]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [297.324,-103.42,-27.3615])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [294.168945,-103.236504,-31.333635]', 'objposition': '[294.169,-103.237,-31.3336]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [294.169,-103.237,-31.3336])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [290.679565,-103.039177,-35.331406]', 'objposition': '[290.68,-103.039,-35.3314]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [290.68,-103.039,-35.3314])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [286.846802,-102.828468,-39.303574]', 'objposition': '[286.847,-102.828,-39.3036]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [286.847,-102.828,-39.3036])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [282.661133,-102.604736,-43.198944]', 'objposition': '[282.661,-102.605,-43.1989]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [282.661,-102.605,-43.1989])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [278.112976,-102.368340,-46.966324]', 'objposition': '[278.113,-102.368,-46.9663]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [278.113,-102.368,-46.9663])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [273.192871,-102.119629,-50.554504]', 'objposition': '[273.193,-102.12,-50.5545]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [273.193,-102.12,-50.5545])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [267.891296,-101.858963,-53.912285]', 'objposition': '[267.891,-101.859,-53.9123]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [267.891,-101.859,-53.9123])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [262.198669,-101.586693,-56.988476]', 'objposition': '[262.199,-101.587,-56.9885]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [262.199,-101.587,-56.9885])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [256.105530,-101.303185,-59.731876]', 'objposition': '[256.106,-101.303,-59.7319]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [256.106,-101.303,-59.7319])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [249.602295,-101.008789,-62.091286]', 'objposition': '[249.602,-101.009,-62.0913]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [249.602,-101.009,-62.0913])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [242.679489,-100.703865,-64.015511]', 'objposition': '[242.679,-100.704,-64.0155]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [242.679,-100.704,-64.0155])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [235.327591,-100.388763,-65.453339]', 'objposition': '[235.328,-100.389,-65.4533]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [235.328,-100.389,-65.4533])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [227.537033,-100.063843,-66.353584]', 'objposition': '[227.537,-100.064,-66.3536]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [227.537,-100.064,-66.3536])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [219.298325,-99.729469,-66.665039]', 'objposition': '[219.298,-99.7295,-66.665]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [219.298,-99.7295,-66.665])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [210.546066,-99.381500,-66.127541]', 'objposition': '[210.546,-99.3815,-66.1275]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [210.546,-99.3815,-66.1275])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [201.241257,-99.016190,-64.567482]', 'objposition': '[201.241,-99.0162,-64.5675]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [201.241,-99.0162,-64.5675])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [191.414047,-98.634468,-62.063522]', 'objposition': '[191.414,-98.6345,-62.0635]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [191.414,-98.6345,-62.0635])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [181.094513,-98.237251,-58.694321]', 'objposition': '[181.095,-98.2373,-58.6943]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [181.095,-98.2373,-58.6943])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [170.312790,-97.825470,-54.538532]', 'objposition': '[170.313,-97.8255,-54.5385]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [170.313,-97.8255,-54.5385])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [159.098984,-97.400047,-49.674820]', 'objposition': '[159.099,-97.4,-49.6748]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [159.099,-97.4,-49.6748])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [147.483215,-96.961922,-44.181839]', 'objposition': '[147.483,-96.9619,-44.1818]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [147.483,-96.9619,-44.1818])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [135.495590,-96.512001,-38.138248]', 'objposition': '[135.496,-96.512,-38.1382]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [135.496,-96.512,-38.1382])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [123.166206,-96.051224,-31.622707]', 'objposition': '[123.166,-96.0512,-31.6227]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [123.166,-96.0512,-31.6227])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [110.525215,-95.580513,-24.713873]', 'objposition': '[110.525,-95.5805,-24.7139]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [110.525,-95.5805,-24.7139])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [97.602684,-95.100792,-17.490404]', 'objposition': '[97.6027,-95.1008,-17.4904]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [97.6027,-95.1008,-17.4904])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [84.428764,-94.612991,-10.030966]', 'objposition': '[84.4288,-94.613,-10.031]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [84.4288,-94.613,-10.031])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [71.033531,-94.118034,-2.414201]', 'objposition': '[71.0335,-94.118,-2.4142]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [71.0335,-94.118,-2.4142])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [57.447140,-93.616844,5.281219]', 'objposition': '[57.4471,-93.6168,5.28122]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [57.4471,-93.6168,5.28122])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [43.699677,-93.110352,12.976634]', 'objposition': '[43.6997,-93.1104,12.9766]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [43.6997,-93.1104,12.9766])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [29.821262,-92.599480,20.593401]', 'objposition': '[29.8213,-92.5995,20.5934]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [29.8213,-92.5995,20.5934])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [15.841985,-92.085152,28.052841]', 'objposition': '[15.842,-92.0852,28.0528]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [15.842,-92.0852,28.0528])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [1.792000,-91.568298,35.276318]', 'objposition': '[1.792,-91.5683,35.2763]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [1.792,-91.5683,35.2763])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-12.298600,-91.049850,42.185146]', 'objposition': '[-12.2986,-91.0499,42.1851]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-12.2986,-91.0499,42.1851])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-26.399704,-90.530724,48.700676]', 'objposition': '[-26.3997,-90.5307,48.7007]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-26.3997,-90.5307,48.7007])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-40.481220,-90.011848,54.744289]', 'objposition': '[-40.4812,-90.0118,54.7443]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-40.4812,-90.0118,54.7443])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-54.512985,-89.494148,60.237255]', 'objposition': '[-54.513,-89.4941,60.2373]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-54.513,-89.4941,60.2373])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-68.464920,-88.978554,65.100967]', 'objposition': '[-68.4649,-88.9786,65.101]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-68.4649,-88.9786,65.101])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-82.306931,-88.465988,69.256760]', 'objposition': '[-82.3069,-88.466,69.2568]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-82.3069,-88.466,69.2568])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-96.008858,-87.957375,72.625954]', 'objposition': '[-96.0089,-87.9574,72.626]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-96.0089,-87.9574,72.626])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-109.540596,-87.453651,75.129921]', 'objposition': '[-109.541,-87.4537,75.1299]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-109.541,-87.4537,75.1299])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-122.872078,-86.955727,76.689972]', 'objposition': '[-122.872,-86.9557,76.69]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-122.872,-86.9557,76.69])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-135.973145,-86.464539,77.227478]', 'objposition': '[-135.973,-86.4645,77.2275]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-135.973,-86.4645,77.2275])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-149.036697,-85.974037,76.867462]', 'objposition': '[-149.037,-85.974,76.8675]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-149.037,-85.974,76.8675])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-162.267227,-85.477844,75.811836]', 'objposition': '[-162.267,-85.4778,75.8118]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-162.267,-85.4778,75.8118])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-175.652023,-84.976372,74.097198]', 'objposition': '[-175.652,-84.9764,74.0972]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-175.652,-84.9764,74.0972])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-189.178345,-84.470055,71.760162]', 'objposition': '[-189.178,-84.4701,71.7602]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-189.178,-84.4701,71.7602])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-202.833466,-83.959312,68.837349]', 'objposition': '[-202.833,-83.9593,68.8373]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-202.833,-83.9593,68.8373])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-216.604691,-83.444572,65.365356]', 'objposition': '[-216.605,-83.4446,65.3654]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-216.605,-83.4446,65.3654])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-230.479263,-82.926247,61.380806]', 'objposition': '[-230.479,-82.9262,61.3808]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-230.479,-82.9262,61.3808])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-244.444489,-82.404755,56.920307]', 'objposition': '[-244.444,-82.4048,56.9203]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-244.444,-82.4048,56.9203])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-258.487640,-81.880539,52.020470]', 'objposition': '[-258.488,-81.8805,52.0205]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-258.488,-81.8805,52.0205])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-272.595978,-81.354004,46.717907]', 'objposition': '[-272.596,-81.354,46.7179]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-272.596,-81.354,46.7179])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-286.756805,-80.825577,41.049225]', 'objposition': '[-286.757,-80.8256,41.0492]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-286.757,-80.8256,41.0492])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-300.957367,-80.295685,35.051041]', 'objposition': '[-300.957,-80.2957,35.051]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-300.957,-80.2957,35.051])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-315.184967,-79.764748,28.759966]', 'objposition': '[-315.185,-79.7647,28.76]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-315.185,-79.7647,28.76])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-329.426849,-79.233185,22.212608]', 'objposition': '[-329.427,-79.2332,22.2126]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-329.427,-79.2332,22.2126])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-343.670319,-78.701424,15.445584]', 'objposition': '[-343.67,-78.7014,15.4456]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-343.67,-78.7014,15.4456])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-357.902679,-78.169891,8.495504]', 'objposition': '[-357.903,-78.1699,8.4955]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-357.903,-78.1699,8.4955])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-372.111145,-77.638992,1.398973]', 'objposition': '[-372.111,-77.639,1.39897]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-372.111,-77.639,1.39897])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-386.283051,-77.109169,-5.807389]', 'objposition': '[-386.283,-77.1092,-5.80739]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-386.283,-77.1092,-5.80739])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-400.405640,-76.580833,-13.086976]', 'objposition': '[-400.406,-76.5808,-13.087]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-400.406,-76.5808,-13.087])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-414.466187,-76.054413,-20.403175]', 'objposition': '[-414.466,-76.0544,-20.4032]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-414.466,-76.0544,-20.4032])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-428.451965,-75.530327,-27.719357]', 'objposition': '[-428.452,-75.5303,-27.7194]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-428.452,-75.5303,-27.7194])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-442.350342,-75.008995,-34.998959]', 'objposition': '[-442.35,-75.009,-34.999]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-442.35,-75.009,-34.999])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-456.148438,-74.490852,-42.205318]', 'objposition': '[-456.148,-74.4909,-42.2053]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-456.148,-74.4909,-42.2053])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-469.833679,-73.976311,-49.301849]', 'objposition': '[-469.834,-73.9763,-49.3018]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-469.834,-73.9763,-49.3018])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-483.393219,-73.465790,-56.251930]', 'objposition': '[-483.393,-73.4658,-56.2519]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-483.393,-73.4658,-56.2519])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-496.814423,-72.959724,-63.018967]', 'objposition': '[-496.814,-72.9597,-63.019]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-496.814,-72.9597,-63.019])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-510.084534,-72.458527,-69.566315]', 'objposition': '[-510.085,-72.4585,-69.5663]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-510.085,-72.4585,-69.5663])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-523.190857,-71.962616,-75.857391]', 'objposition': '[-523.191,-71.9626,-75.8574]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-523.191,-71.9626,-75.8574])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-536.120605,-71.472435,-81.855576]', 'objposition': '[-536.121,-71.4724,-81.8556]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-536.121,-71.4724,-81.8556])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-548.861084,-70.988388,-87.524246]', 'objposition': '[-548.861,-70.9884,-87.5242]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-548.861,-70.9884,-87.5242])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-561.399597,-70.510902,-92.826813]', 'objposition': '[-561.4,-70.5109,-92.8268]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-561.4,-70.5109,-92.8268])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-573.723450,-70.040398,-97.726669]', 'objposition': '[-573.723,-70.0404,-97.7267]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-573.723,-70.0404,-97.7267])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-585.819824,-69.577301,-102.187149]', 'objposition': '[-585.82,-69.5773,-102.187]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-585.82,-69.5773,-102.187])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-597.676086,-69.122040,-106.171715]', 'objposition': '[-597.676,-69.122,-106.172]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-597.676,-69.122,-106.172])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-609.279419,-68.675026,-109.643692]', 'objposition': '[-609.279,-68.675,-109.644]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-609.279,-68.675,-109.644])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-620.617249,-68.236687,-112.566513]', 'objposition': '[-620.617,-68.2367,-112.567]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-620.617,-68.2367,-112.567])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-631.676697,-67.807449,-114.903542]', 'objposition': '[-631.677,-67.8074,-114.904]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-631.677,-67.8074,-114.904])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-642.445129,-67.387726,-116.618179]', 'objposition': '[-642.445,-67.3877,-116.618]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-642.445,-67.3877,-116.618])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-652.909790,-66.977951,-117.673828]', 'objposition': '[-652.91,-66.978,-117.674]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-652.91,-66.978,-117.674])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-663.057983,-66.578537,-118.033829]', 'objposition': '[-663.058,-66.5785,-118.034]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-663.058,-66.5785,-118.034])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-673.023315,-66.183174,-117.765663]', 'objposition': '[-673.023,-66.1832,-117.766]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-673.023,-66.1832,-117.766])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-682.939026,-65.785759,-116.981400]', 'objposition': '[-682.939,-65.7858,-116.981]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-682.939,-65.7858,-116.981])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-692.791687,-65.387070,-115.711403]', 'objposition': '[-692.792,-65.3871,-115.711]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-692.792,-65.3871,-115.711])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-702.567932,-64.987869,-113.986031]', 'objposition': '[-702.568,-64.9879,-113.986]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-702.568,-64.9879,-113.986])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-712.254395,-64.588905,-111.835632]', 'objposition': '[-712.254,-64.5889,-111.836]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-712.254,-64.5889,-111.836])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-721.837585,-64.190964,-109.290581]', 'objposition': '[-721.838,-64.191,-109.291]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-721.838,-64.191,-109.291])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-731.304138,-63.794796,-106.381226]', 'objposition': '[-731.304,-63.7948,-106.381]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-731.304,-63.7948,-106.381])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-740.640686,-63.401169,-103.137924]', 'objposition': '[-740.641,-63.4012,-103.138]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-740.641,-63.4012,-103.138])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-749.833801,-63.010849,-99.591042]', 'objposition': '[-749.834,-63.0108,-99.591]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-749.834,-63.0108,-99.591])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-758.870117,-62.624596,-95.770927]', 'objposition': '[-758.87,-62.6246,-95.7709]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-758.87,-62.6246,-95.7709])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-767.736267,-62.243176,-91.707954]', 'objposition': '[-767.736,-62.2432,-91.708]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-767.736,-62.2432,-91.708])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-776.418762,-61.867355,-87.432465]', 'objposition': '[-776.419,-61.8674,-87.4325]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-776.419,-61.8674,-87.4325])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-784.904297,-61.497894,-82.974831]', 'objposition': '[-784.904,-61.4979,-82.9748]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-784.904,-61.4979,-82.9748])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-793.179382,-61.135563,-78.365395]', 'objposition': '[-793.179,-61.1356,-78.3654]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-793.179,-61.1356,-78.3654])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-801.230713,-60.781116,-73.634529]', 'objposition': '[-801.231,-60.7811,-73.6345]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-801.231,-60.7811,-73.6345])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-809.044800,-60.435329,-68.812592]', 'objposition': '[-809.045,-60.4353,-68.8126]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-809.045,-60.4353,-68.8126])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-816.608337,-60.098957,-63.929932]', 'objposition': '[-816.608,-60.099,-63.9299]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-816.608,-60.099,-63.9299])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-823.907898,-59.772770,-59.016914]', 'objposition': '[-823.908,-59.7728,-59.0169]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-823.908,-59.7728,-59.0169])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-830.930115,-59.457527,-54.103893]', 'objposition': '[-830.93,-59.4575,-54.1039]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-830.93,-59.4575,-54.1039])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-837.661499,-59.153999,-49.221233]', 'objposition': '[-837.661,-59.154,-49.2212]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-837.661,-59.154,-49.2212])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-844.088684,-58.862946,-44.399303]', 'objposition': '[-844.089,-58.8629,-44.3993]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-844.089,-58.8629,-44.3993])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-850.198364,-58.585129,-39.668434]', 'objposition': '[-850.198,-58.5851,-39.6684]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-850.198,-58.5851,-39.6684])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-855.977051,-58.321320,-35.059006]', 'objposition': '[-855.977,-58.3213,-35.059]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-855.977,-58.3213,-35.059])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-861.411377,-58.072273,-30.601358]', 'objposition': '[-861.411,-58.0723,-30.6014]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-861.411,-58.0723,-30.6014])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-866.487915,-57.838764,-26.325880]', 'objposition': '[-866.488,-57.8388,-26.3259]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-866.488,-57.8388,-26.3259])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-871.193359,-57.621548,-22.262905]', 'objposition': '[-871.193,-57.6215,-22.2629]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-871.193,-57.6215,-22.2629])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-875.514221,-57.421391,-18.442785]', 'objposition': '[-875.514,-57.4214,-18.4428]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-875.514,-57.4214,-18.4428])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-879.437073,-57.239059,-14.895906]', 'objposition': '[-879.437,-57.2391,-14.8959]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-879.437,-57.2391,-14.8959])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-882.948669,-57.075317,-11.652590]', 'objposition': '[-882.949,-57.0753,-11.6526]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-882.949,-57.0753,-11.6526])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-886.035461,-56.930931,-8.743241]', 'objposition': '[-886.035,-56.9309,-8.74324]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-886.035,-56.9309,-8.74324])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-888.684143,-56.806660,-6.198191]', 'objposition': '[-888.684,-56.8067,-6.19819]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-888.684,-56.8067,-6.19819])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-890.881287,-56.703266,-4.047797]', 'objposition': '[-890.881,-56.7033,-4.0478]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-890.881,-56.7033,-4.0478])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-892.613464,-56.621521,-2.322430]', 'objposition': '[-892.613,-56.6215,-2.32243]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-892.613,-56.6215,-2.32243])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-893.867371,-56.562187,-1.052420]', 'objposition': '[-893.867,-56.5622,-1.05242]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-893.867,-56.5622,-1.05242])'}], [{'objscale': '[1,1,1]', 'obj': '$Box:Box001 @ [-894.629517,-56.526024,-0.268167]', 'objposition': '[-894.63,-56.526,-0.268167]', 'objname': u'Box001', 'objtype': 'Box', 'objrotation': '(quat 0 0 0 1)', 'objtransform': '(matrix3 [1,0,0] [0,1,0] [0,0,1] [-894.63,-56.526,-0.268167])'}]]

def ls():
    selectedModels = FBModelList()

    topModel = None  # Search all models, not just a particular branch
    selectionState = True  # Return models that are selected, not deselected
    sortBySelectOrder = True  # The last model in the list was selected most recently
    FBGetSelectedModels(selectedModels, topModel, selectionState, sortBySelectOrder)
    obj = []
    for model in selectedModels:
        obj.append(model)
        model, model.LongName
    return obj


def GetLayerIndex(take, layerVariant):
    '''
    Given a variable representing a layer, returns the index of that layer
    within the given take, or -1 if no such layer exists. layerVariant can
    either be an actual layer object, the name of a layer, or, for the sake of
    convenience, a layer's index.
    '''
    # If the layer variant is already an index, we simply return it
    if isinstance(layerVariant, int):
        return layerVariant

    # Otherwise, we need to qualify it to obtain a name
    if isinstance(layerVariant, basestring):
        name = layerVariant
    else:
        name = layerVariant.Name # It must be an FBAnimationLayer

    # Finally, search for the layer by name
    for i in range(0, take.GetLayerCount()):
        if take.GetLayer(i).Name == name:
            return i
    return -1

def CreateNewLayer(take, name):
    '''
    Creates a new layer in the given take, but conveniently allows an initial
    name to be supplied. Returns the new FBAnimationLayer object.
    '''
    # Puzzlingly, this API method doesn't return the new layer
    take.CreateNewLayer()

    # However, new layers are always created at the top of the stack
    layer = take.GetLayer(take.GetLayerCount() - 1)
    layer.Name = name
    return layer

"""
def SetCurrentLayer(take, layerVariant):
    '''
    Given a variable representing a layer (either an index, a name, or an
    actual layer object), makes that layer current.
    '''
    layerIndex = GetLayerIndex(layerOrName)
    assert layerIndex >= 0

    take.SetCurrentLayer(layerIndex)
    """

def SerializeCurve(fcurve):
    '''
    Returns a list of dictionaries representing each of the keys in the given
    FCurve.
    '''
    keyDataList = []

    for key in fcurve.Keys:
        keyData = {
            'time': key.Time.Get(),
            'value': key.Value,
            'interpolation': int(key.Interpolation),
            'tangent-mode': int(key.TangentMode),
            'constant-mode': int(key.TangentConstantMode),
            'left-derivative': key.LeftDerivative,
            'right-derivative': key.RightDerivative,
            'left-weight': key.LeftTangentWeight,
            'right-weight': key.RightTangentWeight
        }

        keyDataList.append(keyData)

    return keyDataList


def GetObjPosRotCV(obj):
    objAPosX = obj.Translation.GetAnimationNode().Nodes[0].FCurve
    objAPosY = obj.Translation.GetAnimationNode().Nodes[1].FCurve
    objAPosZ = obj.Translation.GetAnimationNode().Nodes[2].FCurve
    objARotX = obj.Rotation.GetAnimationNode().Nodes[0].FCurve
    objARotY = obj.Rotation.GetAnimationNode().Nodes[1].FCurve
    objARotZ = obj.Rotation.GetAnimationNode().Nodes[2].FCurve
    return objAPosX, objAPosY, objAPosZ,objARotX,objARotY,objARotZ


def getObjPosVetor(obj):

    posX = []
    posY = []
    posZ = []
    rotX = []
    rotY = []
    rotZ = []
    objposcv = GetObjPosRotCV(obj)
    print(objposcv)
    objposcvX = SerializeCurve(objposcv[0])
    objposcvY = SerializeCurve(objposcv[1])
    objposcvZ = SerializeCurve(objposcv[2])
    objrotcvx = SerializeCurve(objposcv[3])
    objrotcvy = SerializeCurve(objposcv[4])
    objrotcvz = SerializeCurve(objposcv[5])
    for i in range(len(objposcvX)):
        posX.append(objposcvX[i]['value'])
        posY.append(objposcvY[i]['value'])
        posZ.append(objposcvZ[i]['value'])

        rotX.append(objrotcvx[i]['value'])
        rotY.append(objrotcvy[i]['value'])
        rotZ.append(objrotcvz[i]['value'])

    return posX, posY, posZ, rotX, rotY, rotZ


def getrateA(listA):
    ratelist = []
    for i in range(len(listA)):
        if i == 0:
            pass
        else:
            rateValue = abs(listA[i] - listA[i - 1])
            ratelist.append(rateValue)
    return ratelist


def FrameRate(rate, allabs=0):
    frameratelist = []
    for i in rate:
        val = i / allabs
        frameratelist.append(val)
    return frameratelist


def getallabs(rate):
    val = 0
    for i in rate:
        val = i+val

    return val


def getAddLayoutVal(startVal, endVal, allabs, FrameRate):
    startVal = startVal
    endVal = endVal
    allabs = allabs
    FrameRate = FrameRate
    addallabs = endVal - startVal

    addFarmeVal = [startVal]
    for i in range(len(FrameRate)):
        Val = FrameRate[i] * addallabs + startVal
        startVal = Val

        addFarmeVal.append(Val)
    addFarmeVal.append(endVal)
    return addFarmeVal


def applyBlend(name,startvetor,endvetor):
    ObjPosCV = GetObjPosRotCV(name)
    startTime = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
    endTime = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

    ObjPoslist = getObjPosVetor(name)
    for i in ObjPosCV :
        cvcount = 0
        rate = getrateA(ObjPoslist[cvcount])
        allabs = getallabs(rate)
        Frmaeratelist = FrameRate(rate, allabs)
        addVal = getAddLayoutVal(startvetor[cvcount], endvetor[cvcount], allabs, Frmaeratelist)

        for k in range(startTime, endTime):
            i.KeyAdd(FBTime(0, 0, 0, k), addVal[k])
        cvcount = cvcount+1


def AdjustmentBlend_Apply():
    take = FBSystem().CurrentTake
    objs = ls()
    startTime = FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame()
    endTime = FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame()

    allObjAddLayout_StartVetor = []
    allObjAddLayout_EndVetor = []
    allObjVetor = []

    take.SetCurrentLayer(0)
    for obj in objs:
        take.SetCurrentLayer(0)
        take = FBSystem().CurrentTake
        vetorval = getObjPosVetor(obj)
        take.SetCurrentLayer(1)
        startVetor = getObjPosVetor(obj)
        endvetor = getObjPosVetor(obj)

        allObjVetor.append(vetorval)
        allObjAddLayout_StartVetor.append(startVetor)
        allObjAddLayout_EndVetor.append(endvetor)

    print(allObjAddLayout_StartVetor)
    print(allObjAddLayout_EndVetor)
    print("------------------")
    print(len(allObjVetor))

    alladdVal = []
    for obj in objs:
        objcount = len(objs)
        print(objcount)
        objcv = GetObjPosRotCV(obj)


        count = 0
        for i in range(0, 6):
            print(i)
            rate= getrateA( allObjVetor[objcount-1][i])
            allabs = getallabs(rate)
            Frmaeratelist = FrameRate(rate, allabs)
            startval = allObjAddLayout_StartVetor[objcount-1][i][0]
            endVal = allObjAddLayout_EndVetor[objcount-1][i][1]
            print (startval)
            print(endVal)
            addVal = getAddLayoutVal(startval,endVal ,allabs, Frmaeratelist)
            alladdVal.append(addVal)

            print(objcv[count])
            for k in range(startTime, endTime+1):
                objcv[count].KeyAdd(FBTime(0, 0, 0, k), addVal[k])

            count = count + 1
        objcount= objcount +1
    print(objs)


objs = ls()
for obj in objs:
    for comp in FBSystem().Scene.Components:
        comp.Selected = False
    obj.Selected = True
    selecobj = FBModelList()
    topModel = None  # Search all models, not just a particular branch
    selectionState = True  # Return models that are selected, not deselected
    sortBySelectOrder = True  # The last model in the list was selected most recently
    FBGetSelectedModels(selecobj, topModel, selectionState, sortBySelectOrder)
    AdjustmentBlend_Apply()
