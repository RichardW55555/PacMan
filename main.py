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

        walls, ghostDoors, ghostStarts, pellets, warps = loadLevel(allMazes[mazeIndex])

        ghost_colors = ["Red", "Pink", "Cyan", "Orange"]
        ghosts = []

        for i, start_pos in enumerate(ghostStarts):
            col = start_pos[0] // tileSize
            row = start_pos[1] // tileSize

            if i < len(ghost_colors):
                color = ghost_colors[i]
                ghosts.append(Enemy(col, row, color))
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
                        PacMan.requestedDirection = "left"
                    if event.key == K_RIGHT or event.key == K_d:
                        PacMan.requestedDirection = "right"
                    if event.key == K_UP or event.key == K_w:
                        PacMan.requestedDirection = "up"
                    if event.key == K_DOWN or event.key == K_s:
                        PacMan.requestedDirection = "down"
            
            #Check If Reset
            if reset == True:
                break

            #Move
            for ghost in ghosts:
                ghost.move(walls, ghostDoors)
            PacMan.move(walls, ghostDoors)

            #Eat Pellets
            pellets = PacMan.eat(pellets)

            #Warp
            for ghost in ghosts:
                ghost.warp(warps)
            pellets = PacMan.warp(warps, pellets)

            #Check Ghost Collisions
            if PacMan.die(x, y, ghosts, ghostStarts) == True:
                if PacMan.lives == 0:
                    print("You Lose")
                    terminate()
                else:
                    PacMan.currentDirection = ""
                    PacMan.requestedDirection = ""

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
            for ghost in ghosts:
                ghost.draw(screen)
            PacMan.draw(screen)
            for w in walls:
                pygame.draw.rect(screen, "blue", w)
            for d in ghostDoors:
                pygame.draw.rect(screen, "white", d)
            pygame.display.update()

            #Tick
            clock.tick(60)
        
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
