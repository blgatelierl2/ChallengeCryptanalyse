#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def minuscule(c):
    return (ord('a')<=ord(c) and ord(c)<=ord('z'))

def majuscule(c):
    return (ord('A')<=ord(c) and ord(c)<=ord('Z'))

def c2i(c):
    return ord(c)-ord('a')

def i2c(i):
    return chr(i+ord('a'))


class Rotor:
    def __init__(self,permut=[]):
        self.permut = range(26)
        self.permut_inv = range(26)
        self.pos = 0
        self.initpos = 0
        if len(permut)>=26:
            self.permut = permut
            self.calcul_inv()

    def fixe_initpos(self,p):
        self.initpos = p
        self.pos = p

    def reinit(self):
        self.pos = self.initpos

    def calcul_inv(self):
        for i in range(26):
            self.permut_inv[self.permut[i]] = i

    def incr(self):
        self.pos = (self.pos+1)%26

    def chiffre(self,c):
        return i2c((self.permut[(c2i(c)+self.pos)%26]-self.pos+26)%26)

    def chiffre_inv(self,c):
        return i2c((self.permut_inv[(c2i(c)+self.pos)%26]-self.pos+26)%26)


class Reflecteur:
    def __init__(self,permut=[]):
        self.permut = range(26)
        if len(permut)>=26:
            self.permut = permut
            
    def chiffre(self,c):
        return i2c(self.permut[c2i(c)])


class Brouilleur:
    def __init__(self):
        self.permut = [i for i in range(26)]

    def chiffre(self,c):
        return i2c(self.permut[c2i(c)])

    def ajoute_fiche(self,a,b):
        for c in [a,b]:
            if self.permut[c]!=c:
                print >> sys.stderr, "ERREUR brouilleur : il y a déjà une fiche en", c, "!"
                return
        self.permut[a] = b
        self.permut[b] = a

    def retire_fiche(self,a):
        b = self.permut[a]
        if a==b:
            print >> sys.stderr, "ERREUR brouilleur : il n'y a pas de fiche en", a, "!"
            return
        self.permut[a] = a
        self.permut[b] = b


class Enigma:
    def __init__(self):
        s0 = [3,8,7,10,12,6,16,24,11,4,15,14,25,18,23,22,1,20,17,0,21,13,19,2,5,9]
        s1 = [12,22,9,19,2,6,16,0,3,8,7,10,23,24,11,4,15,14,25,21,13,1,20,17,5,18]
        s2 = [19,2,13,23,24,16,15,12,22,4,18,1,11,6,9,14,25,21,20,17,5,0,3,8,7,10]
        subs = [s0,s1,s2]
        self.rotors = [Rotor(subs[i]) for i in range(3)]
        rs0 = [24,20,13,23,18,16,25,21,22,12,19,14,9,2,11,17,5,15,4,10,1,7,8,3,0,6]
        self.reflecteur = Reflecteur(rs0)
        self.brouilleur = Brouilleur()

    def chiffre(self,c):
        d = self.brouilleur.chiffre(self.rotors[0].chiffre_inv(self.rotors[1].chiffre_inv(self.rotors[2].chiffre_inv(self.reflecteur.chiffre(self.rotors[2].chiffre(self.rotors[1].chiffre(self.rotors[0].chiffre(self.brouilleur.chiffre(c)))))))))
        self.rotors[0].incr()
        if self.rotors[0].pos==self.rotors[0].initpos:
            self.rotors[1].incr()
            if self.rotors[1].pos==self.rotors[1].initpos:
                self.rotors[2].incr()
        return d

    def chiffre_mess(self,m):
        l = []
        for  c in m:
            if minuscule(c):
                l.append(self.chiffre(c))
            elif majuscule(c):
                l.append(self.chiffre(c.lower()).upper())
            else:
                l.append(c)
        return ''.join(l)

    def clef(self,(p0,p1,p2)):
        self.rotors[0].fixe_initpos(p0)
        self.rotors[1].fixe_initpos(p1)
        self.rotors[2].fixe_initpos(p2)

    def echange_rotors(self,r1,r2):
        self.rotors[r1],self.rotors[r2] = self.rotors[r2],self.rotors[r1]

    def reinit(self):
        for i in range(3):
            self.rotors[i].reinit()

    def ajoute_fiche(self,a,b):
        self.brouilleur.ajoute_fiche(a,b)

    def retire_fiche(self,a):
        self.brouilleur.retire_fiche(a)
