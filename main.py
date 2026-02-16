import pygame, sys
from pygame.locals import *

width = 438
height = 576

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Score: %s" % (0))
clock = pygame.time.Clock()

class Player:
    def __init__(self, tileSize, mapSize):
        self.position = (int((mapSize[0]//2*tileSize)+(tileSize//2)), int((mapSize[1]//4*tileSize)+(tileSize//2)))
        self.size = 17
        self.score = 0
        self.speed = tileSize
    
    def draw(self):
        pygame.draw.circle(screen, "yellow", self.position, self.size)
    
    def move(self, up, left, down, right, walls):
        position = self.position
        
        if up :
            new_y = position[1] - self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                    return
            position = (position[0], new_y)
        if left:
            new_x = position[0] - self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                    return
            position = (new_x, position[1])
        if down:
            new_y = position[1] + self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                    return
            position = (position[0], new_y)
        if right:
            new_x = position[0] + self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                    return
            position = (new_x, position[1])
        
        self.position = position

def terminate():
    pygame.quit()
    sys.exit()

while True:
    tileSize = 40
    map = [
        "............##............",
        ".####.#####.##.#####.####.",
        ".####.#####.##.#####.####.",
        ".####.#####.##.#####.####.",
        "..........................",
        ".####.##.########.##.####.",
        ".####.##.########.##.####.",
        "......##....##....##......",
        "#####.#####.##.#####.#####",
        "#####.#####.##.#####.#####",
        "#####.##..........##.#####",
        "#####.##.--------.##.#####",
        "#####.##.--------.##.#####",
        ".........--------.........",
        "#####.##.--------.##.#####",
        "#####.##.--------.##.#####",
        "#####.##..........##.#####",
        "#####.##.########.##.#####",
        "#####.##.########.##.#####",
        "............##............",
        ".####.#####.##.#####.####.",
        ".####.#####.##.#####.####.",
        "...##................##...",
        "##.##.##.########.##.##.##",
        "##.##.##.########.##.##.##",
        "......##....##....##......",
        ".##########.##.###########",
        ".##########.##.###########",
        "..........................",
    ]

    walls = []
    pellets = []
    for rowI, row in enumerate(map):
        for colI, char in enumerate(row):
            x = colI*tileSize
            y = rowI*tileSize

            if char == "#":
                walls.append(pygame.Rect(x, y, tileSize, tileSize))
            elif char == ".":
                pellets.append((x+tileSize//2, y+tileSize//2))
    
    up = False
    left = False
    down = False
    right = False

    PacMan = Player(tileSize, (len(map[0]), len(map)))

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
        PacMan.draw()
        for w in walls:
            pygame.draw.rect(screen, "blue", w)
        pygame.display.update()

        #Tick
        clock.tick(10)