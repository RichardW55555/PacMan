import pygame
from constants import *

class Character:
    def __init__(self, startCol, startRow):
        self.position = (
            startCol * tileSize + tileSize // 2, 
            startRow * tileSize + tileSize // 2
        )
        self.size = 10
        self.speed = tileSize
    
    def canMove(self, up, left, down, right, walls, ghostDoors, isPlayer):
        position = self.position
        
        if up:
            new_y = position[1] - self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                    return False
            if isPlayer:
                for d in ghostDoors:
                    if d.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False
        elif left:
            new_x = position[0] - self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                    return False
            if isPlayer:
                for d in ghostDoors:
                    if d.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                        return False
        elif down:
            new_y = position[1] + self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                    return False
            if isPlayer:
                for d in ghostDoors:
                    if d.colliderect(pygame.Rect(self.position[0]-self.size, new_y-self.size, self.size*2, self.size*2)):
                        return False
        elif right:
            new_x = position[0] + self.speed
            for w in walls:
                if w.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                    return False
            if isPlayer:
                for d in ghostDoors:
                    if d.colliderect(pygame.Rect(new_x-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                        return False

        return True