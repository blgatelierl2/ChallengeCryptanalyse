#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, random, os
random.seed()

from enigma import *

## Rejewski
def signature(t):
    sig = []
    i = 0
    while i<len(t):
        if t[i]>=0:
            j = i
            c = 0
            while t[j]>=0:
                sj = j
                j = t[j]
                t[sj] = -1
                c += 1
            sig.append(c)
        i += 1
    sig.sort()
    return sig


def genere_cycles():
    sig2clef = dict()
    e = Enigma()
    t14 = [-1 for i in range(26)]
    t25 = [-1 for i in range(26)]
    t36 = [-1 for i in range(26)]
    rotors = range(3)
    for r0 in range(3):
        if r0>0:
            e.echange_rotors(0,r0) # échange 0 <-> r0
            rotors[0],rotors[r0] = rotors[r0],rotors[0]
        for inv12 in range(2):
            if inv12>0:
                e.echange_rotors(1,2) # échange 1 <-> 2
                rotors[1],rotors[2] = rotors[2],rotors[1]  
            for p0 in range(26):
                for p1 in range(26):
                    for p2 in range(26):
                        for a in range(26):
                            e.clef((p0,p1,p2))
                            m = i2c(a)*6
                            mc = e.chiffre_mess(m)
                            t14[c2i(mc[0])] = c2i(mc[3])
                            t25[c2i(mc[1])] = c2i(mc[4])
                            t36[c2i(mc[2])] = c2i(mc[5])
                        sigs = (tuple(signature(t14)),tuple(signature(t25)),tuple(signature(t36)))
                        cle = (tuple(rotors),(p0,p1,p2))
                        if sigs in sig2clef:
                            sig2clef[sigs].append(cle)
                        else:
                            sig2clef[sigs] = [cle]
            if inv12>0:
                e.echange_rotors(1,2)
                rotors[1],rotors[2] = rotors[2],rotors[1]
        if r0>0:
            e.echange_rotors(0,r0)
            rotors[0],rotors[r0] = rotors[r0],rotors[0]
    return sig2clef

def genere_messages(r,k,fiches,n):
    l = []
    e = Enigma()
    if r[0]!=0:
        e.echange_rotors(0,r[0])
        if r[r[0]]!=0:
            e.echange_rotors(1,2)
    elif r[1]!=1:
        e.echange_rotors(1,2)
    for fiche in fiches:
        e.ajoute_fiche(fiche[0],fiche[1])
    for nb in range(n):
        m = (''.join([i2c(random.randint(0,25)) for i in range(3)]))*2
        e.clef(k)
        cm = e.chiffre_mess(m)
        l.append(cm)
    return l

def rejewski(sig2clef,listmess):
    t14 = [-1 for i in range(26)]
    t25 = [-1 for i in range(26)]
    t36 = [-1 for i in range(26)]
    for m in listmess:
        t14[c2i(m[0])] = c2i(m[3])
        t25[c2i(m[1])] = c2i(m[4])
        t36[c2i(m[2])] = c2i(m[5])
    if (-1 in t14) or (-1 in t25) or (-1 in t36):
        #print "Messages insuffisants pour cryptanalyse !"
        return []
    sigs = (tuple(signature(t14)),tuple(signature(t25)),tuple(signature(t36)))
    return sig2clef[sigs]


## MAIN
def main():
    print "Generation des cycles..."
    sig2clef = genere_cycles()
    clefdujour = tuple([random.randint(0,25) for i in range(3)])
    rotors = tuple(random.sample(range(3),2)) # 1 échange
    print "Clef du jour :", rotors, clefdujour
    messages = genere_messages(clefdujour,250)
    print "Clefs possibles :", rejewski(sig2clef,messages)

def main_sujets():
    sig2clef = genere_cycles()
    for g in range(20):
        while True:
            clefdujour = tuple([random.randint(0,25) for i in range(3)])
            rotors = range(3)
            random.shuffle(rotors)
            rotors = tuple(rotors)
            # NB : il est important de mettre des fiches pour éviter la méthode
            # idiote consistant à brute-forcer sur les configurations de la 
            # machine jusqu'à en trouver une qui décrypte tous les préfixes
            # donnés sous une forme répétitive "abcabc" 
            fiches = random.sample(range(26),12)
            fiches = [(fiches[2*i],fiches[2*i+1]) for i in range(6)]
            messages = genere_messages(rotors,clefdujour,fiches,250)
            rej = rejewski(sig2clef,messages)
            if len(rej)<50 and len(rej)>0:
                break
        print g+1
        print "Clef du jour :", rotors, clefdujour, "+", fiches
        print "Clefs possibles :", rej
        print
        gp_dir = os.path.join('./dest','Groupe'+str(g+1))
        os.mkdir(gp_dir)
        df4_dir = os.path.join(gp_dir,'Defi4')
        os.mkdir(df4_dir)
        f = open(os.path.join(df4_dir,'prefixes.txt'),'w')
        f.write('\n'.join(messages))
        f.close()

main_sujets()
