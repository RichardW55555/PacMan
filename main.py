import sys
import pygame
from player import *
from constants import *
from maze import *
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Score: %s" % (0))
clock = pygame.time.Clock()

def terminate():
    pygame.quit()
    sys.exit()

while True:
    walls = []
    pellets = []
    warps = []
    for rowI, row in enumerate(map):
        for colI, char in enumerate(row):
            x = colI*tileSize
            y = rowI*tileSize

            if char == "#":
                walls.append(pygame.Rect(x, y, tileSize, tileSize))
            elif char == ".":
                pellets.append((x+tileSize//2, y+tileSize//2))
            elif char == "w":
                warps.append((x+tileSize//2, y+tileSize//2))
    
    up = False
    left = False
    down = False
    right = False

    PacMan = Player(tileSize, 13, 23)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #Pressing ESC quits.
                    terminate()
                #Change the keyboard variables.
                if event.key == K_LEFT or event.key == K_a:
                    left = True
                    right = False
                    up = False
                    down = False
                if event.key == K_RIGHT or event.key == K_d:
                    left = False
                    right = True
                    up = False
                    down = False
                if event.key == K_UP or event.key == K_w:
                    left = False
                    right = False
                    up = True
                    down = False
                if event.key == K_DOWN or event.key == K_s:
                    left = False
                    right = False
                    up = False
                    down = True
        
        #Move Player
        PacMan.move(up, left, down, right, walls)

        #Eat Pellets
        pellets = PacMan.eat(tileSize, pellets)

        #Warp
        pellets = PacMan.warp(tileSize, warps, pellets)

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
