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
        self.dotsEaten = 0
        raw_img = pygame.image.load(os.path.join("Assets", "PacMan.png"))
        self.pacman_img = raw_img.convert_alpha()
        self.pacman_img = pygame.transform.scale(self.pacman_img, (self.size*2, self.size*2))
        self.imgDirection = {
            "up": pygame.transform.rotate(self.pacman_img, 270),
            "down": pygame.transform.rotate(self.pacman_img, 90),
            "left": pygame.transform.rotate(self.pacman_img, 0),
            "right": pygame.transform.rotate(self.pacman_img, 180),
            "": pygame.transform.rotate(self.pacman_img, 180)
        }
        self.current_img = self.imgDirection[""]
    
    def move(self, walls, ghostDoors):
        position = self.position
        if self.requestedDirection != "":
            if self.checkCenter() or self.requestedDirection == opposites.get(self.currentDirection):
                movePossible, _ = self.canMove(self.requestedDirection, walls, ghostDoors)
                if movePossible:
                    self.currentDirection = self.requestedDirection
                    self.requestedDirection = ""
        
        movePossible, _ = self.canMove(self.currentDirection, walls, ghostDoors)
        if not movePossible:
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
    
    def eat(self, pellets, energizers):
        newPellets = []
        newEnergizers = []
        energizerEaten = False
        for p in pellets:
            if pygame.Rect(p[0], p[1], 2, 2).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.score+=10
                self.dotsEaten += 1
                # Vunerable ghosts
                continue
            newPellets.append(p)
        pellets = newPellets
        for e in energizers:
            if pygame.Rect(e[0], e[1], 2, 2).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.score+=50
                self.dotsEaten+=1
                energizerEaten = True
                continue
            newEnergizers.append(e)
        energizers = newEnergizers
        pygame.display.set_caption("Score: %s" % (self.score))
        return pellets, energizers, energizerEaten
    
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
    
    def die(self, ghosts, starts):
        for ghost in ghosts:
            if pygame.Rect(ghost.position[0]-ghost.size, ghost.position[1]-ghost.size, ghost.size*2, ghost.size*2).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.lives -= 1
                self.dotsEaten = 0
                self.position = starts["PacMan"]
                self.current_img = self.imgDirection["right"]
                for _, ghost in enumerate(ghosts):
                    ghost.releaseTimer = 0
                    ghost.position = starts[ghost.name]
                    ghost.current_img = ghost.imgDirection[""]
                return True
        return False