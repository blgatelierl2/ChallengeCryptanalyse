#!/usr/bin/env python

# Seuil d'IC pour cryptanalyse
# La valeur a prendre depend de la langue naturelle.
# Ici on est en anglais, 0.066 est une bonne valeur pour l'IC.
# https://fr.wikipedia.org/wiki/Indice_de_co%C3%AFncidence
ICseuil = 0.064


# caractere -> numero
def char2num(c):
    return ord(c)-ord('a')

# numero -> caractere
def num2char(i):
    return chr(i+ord('a'))

# teste si c est un lettre a-z
def estLettre(c):
    return (ord('a')<=ord(c) and ord(c)<=ord('z'))


# Chiffre un message
def chiffre(K,M):
    C = []
    ik = 0
    for i in range(len(M)):
        if estLettre(M[i]):
            C.append(num2char((char2num(M[i])+char2num(K[ik]))%26))
            ik = (ik+1)%len(K)
        else:
            C.append(M[i])
    return ''.join(C)


# Inverse une clef
def inverseClef(K):
    return ''.join([num2char((26-char2num(k))%26) for k in K])


# Dechiffre un message
def dechiffre(K,M):
    return chiffre(inverseClef(K),M)


# Calcule les indices de coincidence des k sous-textes
# dans le tableau IC et les lettres majoritaires dans ces
# sous-textes dans le tableau Lmaj
def IC(k,M):
    ik = 0
    cpt = [[0 for _ in range(26)] for _ in range(k)]
    Lmaj = [0 for _ in range(k)]
    for c in M:
        if estLettre(c):
            n = char2num(c)
            cpt[ik][n] += 1
            if cpt[ik][n]>cpt[ik][Lmaj[ik]]:
                Lmaj[ik] = n
            ik = (ik+1)%k
    ICs = [0. for _ in range(k)]
    for i in range(k):
        N = 0
        for j in range(26):
            ICs[i] += cpt[i][j]*(cpt[i][j]-1)
            N += cpt[i][j]
        ICs[i] /= N*(N-1)
    return ICs,Lmaj


# Cryptanalyse un message
def cryptanalyse(M):
    k = 0
    ICmoy = 0
    while ICmoy<ICseuil:
        k += 1
        ICs,Lmaj = IC(k,M)
        ICmoy = sum(ICs)/len(ICs)
    return ''.join([num2char((Lmaj[i]+22)%26) for i in range(k)])
