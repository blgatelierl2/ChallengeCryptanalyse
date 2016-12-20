#!/opt/local/bin/python2.6
# -*- coding: utf-8 -*-

import sys, Image, pygame, time
from brouillage import *

black = (0,0,0)
white = (255,255,255)
gray = (192,192,192)

def catch_event():
    global step, f
    for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and (event.key in [pygame.K_ESCAPE,pygame.K_SPACE,pygame.K_q])):
            sys.exit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT:
            morph.transforme(f)
            step = (step+1)%phacc.tps_retour
            upscreen()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT:
            morph.transforme(f_inv)
            step = (step-1+phacc.tps_retour)%phacc.tps_retour
            upscreen()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_UP:
            morph.transforme(phacc.iteration(10))
            step = (step+10+phacc.tps_retour)%phacc.tps_retour
            upscreen() 
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_DOWN:
            morph.transforme(phacc.iteration(phacc.tps_retour-10))
            step = (step-10+phacc.tps_retour)%phacc.tps_retour
            upscreen()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_PAGEUP:
            morph.transforme(phacc.iteration(100))
            step = (step+100+phacc.tps_retour)%phacc.tps_retour
            upscreen() 
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_PAGEDOWN:
            morph.transforme(phacc.iteration(phacc.tps_retour-100))
            step = (step-100+phacc.tps_retour)%phacc.tps_retour
            upscreen()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_r:
            init(f)
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_b:
            init(boulanger)
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_p:
            init(photomaton)

def upscreen():
    screen.fill(black)
    mode = morph.image().mode 
    data = morph.image().tostring() 
    img_surf = pygame.image.frombuffer(data, size, mode)
    screen.blit(img_surf, ((w-size[0])/2,(h-size[1])/2))
    font = pygame.font.Font(None, 26)
    text = font.render("Boulanger", 1, gray)
    if f==photomaton:
        text = font.render("Photomaton", 1, gray)
    screen.blit(text, (10,5))
    text = font.render("Temps de retour : "+str(phacc.tps_retour), 1, gray)
    screen.blit(text, (10,25))
    text = font.render("Etape : "+str(step), 1, gray)
    screen.blit(text, (10,45))
    pygame.display.flip()

def init(t):
    global step, morph, phacc, f, f_inv
    step = 0
    f = t
    morph = Morphimage(img.copy())
    phacc = Transformacceleration(f,size)
    f_inv = phacc.inverse()
    upscreen()
 
def main():
    global size, w, h, screen, img
    if len(sys.argv)>1:
        pygame.init()
        w,h = 0,0
        screen = pygame.display.set_mode((w,h),pygame.FULLSCREEN)
        w,h = screen.get_size()
        pygame.mouse.set_visible(False)
        img = Image.open(sys.argv[1])
        size = img.size
        if size[0]%2==1 or size[1]%2==1:
            print "Les dimensions doivent être paires !"
            sys.exit()
        init(boulanger)
        while True:
            catch_event()

    else:
        print "usage: ./exemple path/to/image"

main()
