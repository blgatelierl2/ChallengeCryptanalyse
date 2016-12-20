#!/opt/local/bin/python2.6
# -*- coding: utf-8 -*-

#import Image
from fractions import gcd

def ppcm(x,y):
    return x*y/gcd(x,y)

def photomaton(x,y,w,h):
    return x/2+(x%2)*(w/2), y/2+(y%2)*(h/2)

def photomaton_inv(x,y,w,h):
    if x<w/2:
        xx = x*2
    else:
        xx = 2*(x-w/2)+1
    if y<h/2:
        yy = 2*y
    else:
        yy = 2*(y-h/2)+1
    return xx,yy

def boulanger(x,y,w,h):
    if x<w/2:
        return 2*x+y%2,y/2
    else:
        return 2*(w-1-x)+(1-y%2),h-1-y/2

def boulanger_inv(x,y,w,h):
    if y<h/2:
        return x/2,2*y+x%2
    else:
        return (w-1-x)/2+w/2,2*(h-1-y)+(h-1-x)%2

class Morphimage:
    def __init__(self,img):
        self.ind = 0
        self.w,self.h = img.size
        self.imgs = [img,img.copy()]
        self.pixs = [self.imgs[i].load() for i in range(2)]

    def save(self,path):
        self.imgs[self.ind].save(path)

    def transforme(self,f,n=1):
        for k in range(n):
            nind = (self.ind+1)%2
            for i in range(self.w):
                for j in range(self.h):
                    self.pixs[nind][f(i,j,self.w,self.h)] = self.pixs[self.ind][(i,j)]
            self.ind = nind

    def image(self):
        return self.imgs[self.ind]


class Transformacceleration:
    def __init__(self,f,(w,h)):
        self.f = f
        self.w,self.h = w,h
        self.precalcul()
        
    def precalcul(self):
        self.tps_retour = 1
        self.cycles = [[None for y in range(self.h)] for x in range(self.w)]
        for x0 in range(self.w):
            for y0 in range(self.h):
                if self.cycles[x0][y0]==None:
                    c = []
                    p = 0
                    x,y = x0,y0
                    while self.cycles[x][y]==None:
                        self.cycles[x][y] = (c,p)
                        c.append((x,y))
                        x,y = self.f(x,y,self.w,self.h)
                        p += 1
                    self.tps_retour = ppcm(self.tps_retour,p)

    def iteration(self,n):
        def f_iter(x,y,w,h):
            c,p = self.cycles[x][y]
            return c[(p+n)%len(c)]
        return f_iter

    def inverse(self):
        return self.iteration(self.tps_retour-1)

    def indices(self,n):
        # au lieu de prendre 1 pt par cycle
        # on prend 1 pt pour 1 cycle par période
        # car tous les cycles de même taille
        # sont synchros
        ind = []
        periodes_vues = []
        for x in range(self.w):
            for y in range(self.h):
                c,p = self.cycles[x][y]
                per = len(c)
                if not (per in periodes_vues):
                    periodes_vues.append(per)
                    nx,ny = c[(p+n)%len(c)]
                    ind.append('(%d,%d) est en position (%d,%d)' % (x,y,nx,ny))
        return ind
