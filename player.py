import pygame
from constants import *

class Player:
    def __init__(self, startCol, startRow):
        self.position = (
        startCol * tileSize + tileSize // 2, 
        startRow * tileSize + tileSize // 2
    )
        self.size = 10
        self.score = 0
        self.speed = tileSize
        raw_img = pygame.image.load("PacMan.png")
        self.pacman_img = raw_img.convert_alpha()
        self.pacman_img = pygame.transform.scale(self.pacman_img, (self.size*2, self.size*2))
        self.direction = {
            "up": pygame.transform.rotate(self.pacman_img, 270),
            "down": pygame.transform.rotate(self.pacman_img, 90),
            "left": pygame.transform.rotate(self.pacman_img, 0),
            "right": pygame.transform.rotate(self.pacman_img, 180)
        }
        self.current_img = self.direction["right"]
    
    def draw(self, screen):
        top_left = (self.position[0] - self.size, self.position[1] - self.size)
        screen.blit(self.current_img, top_left)
    
    def move(self, up, left, down, right, walls):
        position = self.position
        
        if up:
            new_y = position[1] - self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                    return False
            position = (position[0], new_y)
            self.current_img = self.direction["up"]
        elif left:
            new_x = position[0] - self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                    return False
            position = (new_x, position[1])
            self.current_img = self.direction["left"]
        elif down:
            new_y = position[1] + self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                    return False
            position = (position[0], new_y)
            self.current_img = self.direction["down"]
        elif right:
            new_x = position[0] + self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                    return False
            position = (new_x, position[1])
            self.current_img = self.direction["right"]
        
        self.position = position

        return True
    
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
    
    def warp(self, warps, pellets):
        for w in warps:
            if pygame.Rect(w[0]-tileSize//2, w[1]-tileSize//2, tileSize, tileSize).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.position = warps[warps.index(w)-1]

                if self.position[0] < width // 2:
                    self.position = (self.position[0] + tileSize, self.position[1])
                else:
                    self.position = (self.position[0] - tileSize, self.position[1])
                
                #Eat Warped On Pellet
                return self.eat(pellets)
        return pellets
