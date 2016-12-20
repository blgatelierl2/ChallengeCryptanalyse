#!/opt/local/bin/python2.6

import os, Image, random
from brouillage import *
random.seed()

src_dir = './source'
dst_dir = './dest/'

def main():
    imgs_src = os.listdir(src_dir)
    for i in range(len(imgs_src)):
        fimg = imgs_src[i]
        img = Image.open(os.path.join(src_dir,fimg))
        morph = Morphimage(img)
        phacc = Transformacceleration(boulanger,img.size)
        print i+1, fimg
        print phacc.tps_retour
        t = random.randint(1,phacc.tps_retour-1)
        morph.transforme(phacc.iteration(t))
        print t
        print
        gp_dir = os.path.join(dst_dir,'Groupe'+str(i+1))
        d5_dir = os.path.join(gp_dir,'Defi5')
        os.mkdir(gp_dir)
        os.mkdir(d5_dir)
        morph.save(os.path.join(d5_dir,'image.png'))
        find = open(os.path.join(d5_dir,'indices.txt'),'w')
        find.write('\n'.join(phacc.indices(t)))
        find.close()
        
main()
