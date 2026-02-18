import sys
import os
import pygame
from player import *
from enemy import *
from constants import *
from maze import *
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Score: %s" % (0))
clock = pygame.time.Clock()

hardReset, reset = False, False

def terminate():
    pygame.quit()
    sys.exit()

mazeIndex = 1

def playLevel(x, y):
    while True:
        global hardReset, reset
        global mazeIndex
    
        up, down, left, right = False, False, False, False

        walls, ghostDoors, ghostStarts, pellets, warps = loadLevel(allMazes[mazeIndex])

        PacMan = Player(x, y)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #Pressing ESC quits.
                        terminate()
                    if event.key == K_r:
                        reset = True
                        mods = pygame.key.get_mods()
                        if mods & KMOD_SHIFT:
                            hardReset = True
                    #Change the keyboard variables.
                    if event.key == K_LEFT or event.key == K_a:
                        if PacMan.canMove(False, True, False, False, walls):
                            left = True
                            right = False
                            up = False
                            down = False
                    if event.key == K_RIGHT or event.key == K_d:
                        if PacMan.canMove(False, False, False, True, walls):
                            left = False
                            right = True
                            up = False
                            down = False
                    if event.key == K_UP or event.key == K_w:
                        if PacMan.canMove(True, False, False, False, walls):
                            left = False
                            right = False
                            up = True
                            down = False
                    if event.key == K_DOWN or event.key == K_s:
                        if PacMan.canMove(False, False, True, False, walls):
                            left = False
                            right = False
                            up = False
                            down = True
            
            #Check If Reset
            if reset == True:
                break

            #Move Player
            PacMan.move(up, left, down, right, walls)

            #Eat Pellets
            pellets = PacMan.eat(pellets)

            #Warp
            pellets = PacMan.warp(warps, pellets)

            #Check If Win
            if len(pellets) == 0:
                if mazeIndex+1 in allMazes:
                    mazeIndex += 1
                else:
                    print("You Win")
                    terminate()
                break

            #Draw Screen
            screen.fill("black")
            for p in pellets:
                pygame.draw.circle(screen, "white", p, 2)
            PacMan.draw(screen)
            for w in walls:
                pygame.draw.rect(screen, "blue", w)
            pygame.display.update()

            #Tick
            clock.tick(10)
        
        if hardReset == True:
            hardReset, reset = False, False
            mazeIndex = 1
            break
        if reset == True:
            reset = False
            break

def main():
    playLevel(13, 23)

if __name__ == "__main__":
    while True:
        main()
