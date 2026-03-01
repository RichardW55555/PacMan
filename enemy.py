import pygame
import os
import random
from character import *
from constants import *

class Enemy(Character):
    def __init__(self, screen, startCol, startRow, name):
        super().__init__(screen, startCol, startRow, False)
        self.movePriority = ["up", "left", "down", "right"]
        self.name = name
        self.releaseTimer = 0
        self.releaseThreshold = 0
        match self.name:
            case "Pinky":
                self.releaseThreshold = 60
            case "Inky":
                self.releaseThreshold = 180
            case "Clyde":
                self.releaseThreshold = 300
        ghosts = pygame.image.load(os.path.join("Assets", "Ghosts.png")).convert_alpha()
        ghostCoords = {
            "Blinky": {
                "up": (19, 0),
                "left": (19, 19),
                "down": (0, 19),
                "right": (0, 0)
            },
            "Inky": {
                "up": (59, 0),
                "left": (59, 19),
                "down": (40, 19),
                "right": (40, 0)
            },
            "Pinky": {
                "up": (19, 39),
                "left": (19, 58),
                "down": (0, 58),
                "right": (0, 39)
            },
            "Clyde": {
                "up": (59, 39),
                "left": (59, 58),
                "down": (40, 58),
                "right": (40, 39)
            }
        }
        ghost = ghostCoords[self.name]
        self.imgDirection = {
            "up": self.getGhost(ghosts, ghost, "up"),
            "left": self.getGhost(ghosts, ghost, "left"),
            "down": self.getGhost(ghosts, ghost, "down"),
            "right": self.getGhost(ghosts, ghost, "right"),
            "": self.getGhost(ghosts, ghost, "right")
        }
        self.current_img = self.imgDirection["right"]
    
    def getGhost(self, ghosts, ghost, direction):
        ghostRect = pygame.Rect(ghost[direction][0]*checkerSquare, ghost[direction][1]*checkerSquare, 160, 160)
        ghostImg = ghosts.subsurface(ghostRect)
        ghostImg = pygame.transform.smoothscale(ghostImg, (self.size*2, self.size*2))
        return ghostImg
    
    def move(self, walls, ghostDoors, target):
        if self.releaseTimer < self.releaseThreshold:
            self.draw("left")
            self.draw("right")
            return
        position = self.position
        opposite = opposites.get(self.currentDirection)

        match self.name:
            case "Blinky": #Chase
                if self.checkCenter():
                    directions = {
                        "up": 0,
                        "left": 0,
                        "down": 0,
                        "right": 0
                    }
                    if opposite in directions:
                        directions.pop(opposite)
                    newDirections = dict()
                    for direction, _ in directions.items():
                        movePossible, distance = self.canMove(direction, walls, ghostDoors, target.position[0], target.position[1], tileSize)
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
                            self.currentDirection = opposite
                    else:
                        self.currentDirection = opposite
            case "Pinky": #Intercept
                if self.checkCenter():
                    targetx, targety = target.position
                    if target.currentDirection == "up":
                        targety -= 4 * tileSize
                    elif target.currentDirection == "down":
                        targety += 4 * tileSize
                    elif target.currentDirection == "left":
                        targetx -= 4 * tileSize
                    elif target.currentDirection == "right":
                        targetx += 4 * tileSize
                    directions = {
                        "up": 0,
                        "left": 0,
                        "down": 0,
                        "right": 0
                    }
                    if opposite in directions:
                        directions.pop(opposite)
                    newDirections = dict()
                    for direction, _ in directions.items():
                        movePossible, distance = self.canMove(direction, walls, ghostDoors, targetx, targety, tileSize)
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
                            self.currentDirection = opposite
                    else:
                        self.currentDirection = opposite
            case "Inky": #Unpredictable
                if self.checkCenter():
                    directions = ["up", "left", "down", "right"]
                    if opposite in directions:
                        directions.remove(opposite)
                    newDirections = []
                    for direction in directions:
                        movePossible, _ = self.canMove(direction, walls, ghostDoors)
                        if movePossible:
                            newDirections.append(direction)
                    directions = newDirections
                    if len(directions) != 0:
                        self.currentDirection = random.choice(directions)
                    else:
                        self.currentDirection = opposite
            case "Clyde": #Random
                if self.checkCenter():
                    directions = ["up", "left", "down", "right"]
                    if opposite in directions:
                        directions.remove(opposite)
                    newDirections = []
                    for direction in directions:
                        movePossible, _ = self.canMove(direction, walls, ghostDoors)
                        if movePossible:
                            newDirections.append(direction)
                    directions = newDirections
                    if len(directions) != 0:
                        self.currentDirection = random.choice(directions)
                    else:
                        self.currentDirection = opposite
        
        
        
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
        self.releaseTimer += 1
    
    def warp(self, warps):
        for w in warps:
            if pygame.Rect(w[0]-tileSize//2, w[1]-tileSize//2, tileSize, tileSize).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.position = warps[warps.index(w)-1]

                if self.position[0] < width // 2:
                    self.position = (self.position[0] + tileSize, self.position[1])
                else:
                    self.position = (self.position[0] - tileSize, self.position[1])