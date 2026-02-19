import pygame
from constants import *

class Character:
    def __init__(self, startCol, startRow):
        self.position = (
            startCol * tileSize + tileSize // 2, 
            startRow * tileSize + tileSize // 2
        )
        self.size = 10
        self.speed = 5
        self.currentDirection = ""
        
    def canMove(self, direction, walls, ghostDoors, isPlayer):
        position = self.position

        obsticles = []
        obsticles += walls
        if isPlayer:
            obsticles += ghostDoors
        
        match direction:
            case "up":
                new_y = position[1] - self.speed - 3
                for o in obsticles:
                    if o.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False
            case "left":
                new_x = position[0] - self.speed - 3
                for o in obsticles:
                    if o.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                        return False
            case "down":
                new_y = position[1] + self.speed + 3
                for o in obsticles:
                    if o.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False
            case "right":
                new_x = position[0] + self.speed + 3
                for o in obsticles:
                    if o.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                        return False

        return True