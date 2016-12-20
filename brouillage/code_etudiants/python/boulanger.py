#!/usr/bin/python
# -*- coding: utf-8 -*-

# Nécessite la bibliothèque Python Imaging Library (PIL)
# Package python-imaging sous Debian/Ubuntu
import sys, Image

def boulanger(x,y,w,h):
    if x<w/2:
        return 2*x+y%2,y/2
    else:
        return 2*(w-1-x)+(1-y%2),h-1-y/2

def transforme(pix_src,pix_dst,(w,h)):
    for i in range(w):
        for j in range(h):
            pix_dst[boulanger(i,j,w,h)] = pix_src[(i,j)]

def main():
    if len(sys.argv)>1:
        img = Image.open(sys.argv[1])
        img2 = Image.new(img.mode,img.size)
        pix = img.load()
        pix2 = img2.load()
        transforme(pix,pix2,img.size)
        img2.save("out.png")
    else:
        print "usage : python boulanger.py <monimage>\n(produit un fichier out.png)"

main()
