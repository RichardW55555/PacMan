import pygame, sys
from pygame.locals import *

width = 438
height = 576

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Score: %s" % (0))
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.position = (int(width//2), int(((height/4)*2.8)//1))
        self.size = 17
        self.score = 0
    
    def draw(self):
        pygame.draw.circle(screen, "yellow", self.position, self.size)
    
    def move(self, up, left, down, right):
        position = self.position
        
        if up :
            new_y = position[1] - 5
            if new_y < 0:
                return
            position = (position[0], new_y)
        if left:
            new_x = position[0] - 5
            if new_x < 0:
                return
            position = (new_x, position[1])
        if down:
            new_y = position[1] + 5
            if new_y > height:
                return
            position = (position[0], new_y)
        if right:
            new_x = position[0] + 5
            if new_x > width:
                return
            position = (new_x, position[1])
        
        self.position = position

def terminate():
    pygame.quit()
    sys.exit()

while True:
    up = False
    left = False
    down = False
    right = False
    PacMan = Player()

    pellets = []
    for x in range(20, width, 20):
        for y in range(20, height, 20):
            pellets.append((x, y))
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
        PacMan.move(up, left, down, right)

        #Eat Pellets
        newPellets = []
        for p in pellets:
            if pygame.Rect(p[0], p[1], 2, 2).colliderect(pygame.Rect(PacMan.position[0]-PacMan.size, PacMan.position[1]-PacMan.size, PacMan.size*2, PacMan.size*2)):
                PacMan.score+=1
                continue
            newPellets.append(p)
        pellets = newPellets
        pygame.display.set_caption("Score: %s" % (PacMan.score))

        #Draw Screen
        screen.fill("black")
        for p in pellets:
            pygame.draw.circle(screen, "white", p, 2)
        #PacMan.draw()
        pygame.display.update()

        #Tick
        clock.tick(60)