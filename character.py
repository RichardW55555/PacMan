import pygame
from constants import *

class Character:
    def __init__(self, screen, startCol, startRow, isPlayer):
        self.screen = screen
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
        self.imgDirection = {
            "up": None,
            "down": None,
            "left": None,
            "right": None,
            "": None
        }
    
    def checkCenter(self):
        return ((self.position[0] - 15) % 30 == 0 and (self.position[1] - 15) % 30 == 0)
    
    def findDistance(self, x1, y1, targetx, targety):
        dx = targetx - x1
        dy = targety - y1
        return ((dx**2)+(dy**2))**0.5
        
    def canMove(self, direction, walls, ghostDoors, targetx=None, targety=None, lookDistance=None):
        position = self.position
        distance = 0
        if lookDistance is None:
            lookDistance = 10
        
        match direction:
            case "up":
                new_y = position[1] - lookDistance
                for w in walls:
                    if w.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False, 0
                if targetx is not None and targety is not None:
                    distance = self.findDistance(self.position[0], new_y, targetx, targety)
            case "left":
                new_x = position[0] - lookDistance
                for w in walls:
                    if w.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                        return False, 0
                if targetx is not None and targety is not None:
                    distance = self.findDistance(new_x, self.position[1], targetx, targety)
            case "down":
                new_y = position[1] + lookDistance
                for w in walls:
                    if w.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False, 0
                for d in ghostDoors:
                    if d.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False, 0
                if targetx is not None and targety is not None:
                    distance = self.findDistance(self.position[0], new_y, targetx, targety)
            case "right":
                new_x = position[0] + lookDistance
                for w in walls:
                    if w.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                        return False, 0
                if targetx is not None and targety is not None:
                    distance = self.findDistance(new_x, self.position[1], targetx, targety)

        return True, distance
    
    def draw(self, direction=None):
        if direction == None:
            direction = self.currentDirection
        top_left = (self.position[0] - self.size, self.position[1] - self.size)
        self.screen.blit(self.imgDirection[direction], top_left)