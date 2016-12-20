#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, random
random.seed()

def lettre(c):
    return ord('a')<=ord(c) and ord(c)<=ord('z')

def c2i(c):
    return ord(c)-ord('a')

def i2c(i):
    return chr(i+ord('a'))

def compter(m):
    comptes = [0 for i in range(26)]
    for c in m:
        if lettre(c):
            comptes[c2i(c)] += 1
    return sorted([(i2c(i),comptes[i]) for i in range(26)], key=lambda x: x[1])

def autosub(cpts):
    #statsfr = ['e','a','i','s','t','n','r','u','l','o','d','m','p','c','v','q','g','b','f','j','h','z','x','y','k','w']
    statsfr = ['e','a','s','i','n','t','r','l','u','o','d','c','p','m','v','g','f','b','q','h','x','j','y','z','k','w']
    d = dict()
    for i in range(26):
        d[cpts[i][0]] = statsfr[25-i]
    return d

def filtre_accents(m):
    d = {'é':'e', 'É':'e', 'è':'e', 'È':'e', 'ë':'e', 'Ë':'e', 'ê':'e', 'Ê':'e', 'à':'a', 'À':'a', 'â':'a', 'Â':'a', 'ù':'u', 'Ù':'u', 'ü':'u', 'Ü':'u', 'û':'u', 'Û':'u', 'ï':'i', 'Ï':'i', 'î':'i', 'Î':'i', 'ç':'c', 'Ç':'c', 'ñ':'n', 'Ñ':'n'}
    for c in d:
        m = m.replace(c,d[c])
    return m

def main():
    if len(sys.argv)>1:
        alpha = map(i2c,range(26))
        random.shuffle(alpha)
        f = open(sys.argv[1],'r')
        message = f.read().lower()
        message = filtre_accents(message)
        message = ''.join([c for c in message if lettre(c)])
        f.close()
        crypt = ''.join([alpha[c2i(c)] for c in message])
        print crypt
        d = autosub(compter(crypt))
        decrypt = ''.join([d[c] for c in crypt])
        print decrypt

def main_sujets():
    src_dir = './source'
    dst_dir = './dest'
    txts = os.listdir(src_dir)
    for g in range(len(txts)):
        f = open(os.path.join(src_dir,txts[g]),'r')
        mess = f.read().lower()
        f.close()
        mess = filtre_accents(mess)
        mess = ''.join([c for c in mess if lettre(c)])

        alpha = map(i2c,range(26))
        random.shuffle(alpha)
        crypt = ''.join([alpha[c2i(c)] for c in mess])
        print g+1, txts[g]
        print ''.join(alpha)
        print

        gp_dir = os.path.join(dst_dir,'Groupe'+str(g+1))
        os.mkdir(gp_dir)
        df1_dir = os.path.join(gp_dir,'Defi1')
        os.mkdir(df1_dir)
        
        fcrypt = open(os.path.join(df1_dir,'message.txt'),'w')
        fcrypt.write(crypt)
        fcrypt.close()

        d = autosub(compter(crypt))
        decrypt = ''.join([d[c] for c in crypt])
        
        fdecrypt = open(os.path.join(dst_dir,'decrypt'+str(g+1)),'w')
        fdecrypt.write(decrypt)
        fdecrypt.close()

main_sujets()
