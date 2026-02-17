import pygame
from constants import *

class Player:
    def __init__(self, tileSize, startCol, startRow):
        self.position = (
        startCol * tileSize + tileSize // 2, 
        startRow * tileSize + tileSize // 2
    )
        self.size = 10
        self.score = 0
        self.speed = tileSize
    
    def draw(self, screen):
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
    
    def eat(self, pellets):
        newPellets = []
        for p in pellets:
            if pygame.Rect(p[0], p[1], 2, 2).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.score+=1
                continue
            newPellets.append(p)
        pellets = newPellets
        pygame.display.set_caption("Score: %s" % (self.score))
        return pellets
    
    def warp(self, tileSize, warps, pellets):
        for w in warps:
            if pygame.Rect(w[0], w[1], tileSize, tileSize).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.position = warps[warps.index(w)-1]

                if self.position[0] < width // 2:
                    self.position = (self.position[0] + tileSize, self.position[1])
                else:
                    self.position = (self.position[0] - tileSize, self.position[1])
                
                #Eat Warped On Pellet
                return self.eat(pellets)
        return pellets
