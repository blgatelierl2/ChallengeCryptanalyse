#!/opt/local/bin/python2.6
# -*- coding: utf-8 -*-

import sys, Image
from brouillage import *

def main():
    if len(sys.argv)>1:
        img = Image.open(sys.argv[1])
        morph = Morphimage(img)
        f = boulanger
        phacc = Transformacceleration(f,img.size)
        print phacc.tps_retour
        t = 49582534273700907791496099863541103249876
        morph.transforme(phacc.iteration(phacc.tps_retour-t))
        morph.save('out.png')
        #print '\n'.join(phacc.indices(phacc.tps_retour/2))
    else:
        print "usage: ./exemple path/to/image"

main()
