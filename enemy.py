import pygame
import os
import random
from character import *
from constants import *

class Enemy(Character):
    def __init__(self, startCol, startRow, name):
        super().__init__(startCol, startRow, False)
        self.movePriority = ["up", "left", "down", "right"]
        self.name = name
        self.color = ""
        if name == "Blinky":
            self.color = "Red"
        elif name == "Pinky":
            self.color = "Pink"
        elif name == "Inky":
            self.color = "Cyan"
        elif name == "Clyde":
            self.color = "Orange"
        raw_img = pygame.image.load(os.path.join("Assets", f"{self.color} Ghost.png"))
        self.ghost_img = raw_img.convert_alpha()
        self.ghost_img = pygame.transform.scale(self.ghost_img, (self.size*2, self.size*2))
    
    def draw(self, screen):
        top_left = (self.position[0] - self.size, self.position[1] - self.size)
        screen.blit(self.ghost_img, top_left)
    
    def move(self, walls, ghostDoors, target):
        position = self.position

        if self.name == "Blinky": #Chase
            if self.checkCenter():
                directions = {
                    "up": 0,
                    "left": 0,
                    "down": 0,
                    "right": 0
                }
                opposite = opposites.get(self.currentDirection)
                if opposite in directions:
                    directions.pop(opposite)
                newDirections = dict()
                for direction, _ in directions.items():
                    movePossible, distance = self.canMove(direction, walls, ghostDoors, False, target, tileSize)
                    if movePossible:
                        newDirections[direction] = distance
                directions = newDirections
                if len(directions) != 0:
                    minDistance = min(directions.values())
                    minDistances = [k for k, v in directions.items() if v == minDistance]
                    if len(minDistances) != 0:
                        for p in self.movePriority:
                            if p in minDistances:
                                self.currentDirection = p
                                break
                    else:
                        self.currentDirection = opposites.get(self.currentDirection)
                else:
                    self.currentDirection = opposites.get(self.currentDirection)
        elif self.name == "Pinky": #Intercept
            pass
        elif self.name == "Inky": #Unpredictable
            if self.checkCenter():
                directions = ["up", "left", "down", "right"]
                opposite = opposites.get(self.currentDirection)
                if opposite in directions:
                    directions.remove(opposite)
                newDirections = []
                for direction in directions:
                    movePossible, _ = self.canMove(direction, walls, ghostDoors, False)
                    if movePossible:
                        newDirections.append(direction)
                directions = newDirections
                self.currentDirection = random.choice(directions)
        elif self.name == "Clyde": #Random
            if self.checkCenter():
                directions = ["up", "left", "down", "right"]
                opposite = opposites.get(self.currentDirection)
                if opposite in directions:
                    directions.remove(opposite)
                newDirections = []
                for direction in directions:
                    movePossible, _ = self.canMove(direction, walls, ghostDoors, False)
                    if movePossible:
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