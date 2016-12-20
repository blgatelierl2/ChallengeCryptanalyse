#!/usr/bin/python
# -*- coding: utf-8 -*-

import enigma

def exemple_chiffrage_simple():
    machine = enigma.Enigma()

    # Clef
    machine.echange_rotors(0,2) # échange des rotors 1 et 3
    machine.clef((15,2,6)) # positions des rotors
    machine.ajoute_fiche(2,8)
    machine.ajoute_fiche(6,15)
    machine.ajoute_fiche(22,10)
    machine.ajoute_fiche(12,24)

    # Message
    message = "ceci est un test"
    print "Message à chiffrer :", message

    # Chiffrage et déchiffrage
    mess_crypt = machine.chiffre_mess(message)
    print "Message chiffré :", mess_crypt
    machine.reinit()
    decrypt = machine.chiffre_mess(mess_crypt)
    print "Message déchiffré :", decrypt


def exemple_chiffrage_allemand():
    machine = enigma.Enigma()

    # Clef du jour
    machine.echange_rotors(0,2) # échange des rotors 1 et 3
    clef_du_jour = (15,2,6)  # positions pour la clef du jour

    # Message et clef choisie
    message = "ceci est un test"
    print "Message à chiffrer :", message
    clef_choisie = (2,7,22)
    print "Clef choisie :", clef_choisie
    prefixe = ''.join(map(enigma.i2c,list(clef_choisie)))*2
    print "Prefixe à ajouter :", prefixe

    # Chiffrage
    machine.clef(clef_du_jour)
    mess_crypt = machine.chiffre_mess(prefixe)
    machine.clef(clef_choisie)
    mess_crypt += machine.chiffre_mess(message)
    print "Message complet chiffré :", mess_crypt

    # Déchiffrage
    machine.clef(clef_du_jour)
    pref_decrypt = machine.chiffre_mess(mess_crypt[:6])
    print "Préfixe déchiffré :", pref_decrypt
    clef_decrypt = tuple(map(enigma.c2i,pref_decrypt[:3]))
    print "Clef choisie déchiffrée :", clef_decrypt
    machine.clef(clef_decrypt)
    decrypt = machine.chiffre_mess(mess_crypt[6:])
    print "Message déchiffré :", decrypt


def main():
    exemple_chiffrage_simple()
    print
    exemple_chiffrage_allemand()

main()
