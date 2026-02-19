import pygame
import os
import random
from character import *
from constants import *

class Enemy(Character):
    def __init__(self, startCol, startRow, color):
        super().__init__(startCol, startRow)
        raw_img = pygame.image.load(os.path.join("Assets", f"{color} Ghost.png"))
        self.ghost_img = raw_img.convert_alpha()
        self.ghost_img = pygame.transform.scale(self.ghost_img, (self.size*2, self.size*2))
    
    def draw(self, screen):
        top_left = (self.position[0] - self.size, self.position[1] - self.size)
        screen.blit(self.ghost_img, top_left)
    
    def move(self, walls, ghostDoors):
        position = self.position

        if ((self.position[0] - 15) % 30 == 0 and (self.position[1] - 15) % 30 == 0):
            directions = ["up", "left", "down", "right"]
            opposite = opposites.get(self.currentDirection)
            if opposite in directions:
                directions.remove(opposite)
            newDirections = []
            for direction in directions:
                if self.canMove(direction, walls, ghostDoors, False):
                    newDirections.append(direction)
            directions = newDirections
            self.currentDirection = random.choice(directions)
        
        match self.currentDirection:
            case "up":
                new_y = position[1] - self.speed
                position = (position[0], new_y)
            case "left":
                new_x = position[0] - self.speed
                position = (new_x, position[1])
            case "down":
                new_y = position[1] + self.speed
                position = (position[0], new_y)
            case "right":
                new_x = position[0] + self.speed
                position = (new_x, position[1])
        
        self.position = position
    
    def warp(self, warps):
        for w in warps:
            if pygame.Rect(w[0]-tileSize//2, w[1]-tileSize//2, tileSize, tileSize).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.position = warps[warps.index(w)-1]

                if self.position[0] < width // 2:
                    self.position = (self.position[0] + tileSize, self.position[1])
                else:
                    self.position = (self.position[0] - tileSize, self.position[1])