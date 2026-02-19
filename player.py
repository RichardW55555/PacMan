import pygame
import os
from character import *
from constants import *

class Player(Character):
    def __init__(self, startCol, startRow):
        super().__init__(startCol, startRow)
        self.requestedDirection = ""
        self.lives = 3
        self.score = 0
        raw_img = pygame.image.load(os.path.join("Assets", "PacMan.png"))
        self.pacman_img = raw_img.convert_alpha()
        self.pacman_img = pygame.transform.scale(self.pacman_img, (self.size*2, self.size*2))
        self.imgDirection = {
            "up": pygame.transform.rotate(self.pacman_img, 270),
            "down": pygame.transform.rotate(self.pacman_img, 90),
            "left": pygame.transform.rotate(self.pacman_img, 0),
            "right": pygame.transform.rotate(self.pacman_img, 180)
        }
        self.current_img = self.imgDirection["right"]
    
    def draw(self, screen):
        top_left = (self.position[0] - self.size, self.position[1] - self.size)
        screen.blit(self.current_img, top_left)
    
    def move(self, walls, ghostDoors):
        position = self.position
        if self.requestedDirection != "":
            if ((self.position[0] - 15) % 30 == 0 and (self.position[1] - 15) % 30 == 0) or self.requestedDirection == opposites.get(self.currentDirection):
                if self.canMove(self.requestedDirection, walls, ghostDoors, True):
                    self.currentDirection = self.requestedDirection
                    self.requestedDirection = ""
        
        if not self.canMove(self.currentDirection, walls, ghostDoors, True):
            return
        
        match self.currentDirection:
            case "up":
                new_y = position[1] - self.speed
                position = (position[0], new_y)
                self.current_img = self.imgDirection["up"]
            case "left":
                new_x = position[0] - self.speed
                position = (new_x, position[1])
                self.current_img = self.imgDirection["left"]
            case "down":
                new_y = position[1] + self.speed
                position = (position[0], new_y)
                self.current_img = self.imgDirection["down"]
            case "right":
                new_x = position[0] + self.speed
                position = (new_x, position[1])
                self.current_img = self.imgDirection["right"]
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
    
    def die(self, x, y, ghosts, ghostStarts):
        for ghost in ghosts:
            if pygame.Rect(ghost.position[0]-ghost.size//2, ghost.position[1]-ghost.size//2, tileSize, tileSize).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.lives -= 1
                self.position = (
                    x * tileSize + tileSize // 2, 
                    y * tileSize + tileSize // 2
                )
                for i, ghost in enumerate(ghosts):
                    ghost.position = ghostStarts[i]
                return True
        return False