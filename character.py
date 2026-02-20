import pygame
from constants import *

class Character:
    def __init__(self, startCol, startRow, isPlayer):
        self.position = (
            startCol * tileSize + tileSize // 2, 
            startRow * tileSize + tileSize // 2
        )
        if not isPlayer:
            self.position = (
                startCol,
                startRow
            )
        self.size = 10
        self.speed = 5
        self.currentDirection = ""
    
    def checkCenter(self):
        return ((self.position[0] - 15) % 30 == 0 and (self.position[1] - 15) % 30 == 0)
    
    def findDistance(self, x1, y1, targetX, targetY):
        dx = targetX - x1
        dy = targetY - y1
        return ((dx**2)+(dy**2))**0.5
        
    def canMove(self, direction, walls, ghostDoors, isPlayer, target=None, lookDistance=None):
        position = self.position
        distance = 0
        if lookDistance is None:
            lookDistance = self.speed

        obsticles = []
        obsticles += walls
        if isPlayer:
            obsticles += ghostDoors
        
        match direction:
            case "up":
                new_y = position[1] - self.speed - lookDistance
                for o in obsticles:
                    if o.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False, 0
                if target:
                    distance = self.findDistance(self.position[0], new_y, target.position[0], target.position[1])
            case "left":
                new_x = position[0] - self.speed - lookDistance
                for o in obsticles:
                    if o.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                        return False, 0
                if target:
                    distance = self.findDistance(new_x, self.position[1], target.position[0], target.position[1])
            case "down":
                new_y = position[1] + self.speed + lookDistance
                for o in obsticles:
                    if o.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False, 0
                if target:
                    distance = self.findDistance(self.position[0], new_y, target.position[0], target.position[1])
            case "right":
                new_x = position[0] + self.speed + lookDistance
                for o in obsticles:
                    if o.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                        return False, 0
                if target:
                    distance = self.findDistance(new_x, self.position[1], target.position[0], target.position[1])

        return True, distance