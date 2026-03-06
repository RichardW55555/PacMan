import pygame
import os
import random
from character import *
from constants import *

class Enemy(Character):
    def __init__(self, startCol, startRow, name, sounds):
        super().__init__(startCol, startRow, 5, sounds)
        self.movePriority = ["up", "left", "down", "right"]
        self.name = name
        self.releaseTimer = 0
        self.releaseThreshold = 0
        self.dotRelease = 0
        match self.name:
            case "Pinky":
                self.releaseThreshold = 240
                self.dotRelease = 5
            case "Inky":
                self.releaseThreshold = 480
                self.dotRelease = 30
            case "Clyde":
                self.releaseThreshold = 720
                self.dotRelease = 60
        self.scaredTimer = 0
        ghosts = pygame.image.load(os.path.join("Assets", "Images", "Ghosts.png")).convert_alpha()
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
        self.current_img = self.imgDirection[""]
    
    def getGhost(self, ghosts, ghost, direction):
        ghostRect = pygame.Rect(ghost[direction][0]*checkerSquare, ghost[direction][1]*checkerSquare, 160, 160)
        ghostImg = ghosts.subsurface(ghostRect)
        ghostImg = pygame.transform.smoothscale(ghostImg, (self.size*2, self.size*2))
        return ghostImg
    
    def pathfindToTarget(self, walls, ghostDoors, opposite, targetx, targety):
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
    
    def move(self, walls, ghosts, ghostDoors, target):
        self.releaseTimer += 1
        if not (self.releaseTimer >= self.releaseThreshold or target.dotsEaten >= self.dotRelease):
            if (self.releaseTimer // 15) % 2 == 0:
                self.current_img = self.imgDirection["up"]
            else:
                self.current_img = self.imgDirection["down"]
            return
        position = self.position
        if self.checkCenter():
            opposite = opposites.get(self.currentDirection)
            if self.scaredTimer > 0:
                self.scaredTimer -= 1
                directions = ["up", "left", "down", "right"]
                if opposite in directions:
                    directions.pop(opposite)
                newDirections = []
                for direction in directions:
                    movePossible, _ = self.canMove(direction, walls, ghostDoors)
                    if movePossible:
                        newDirections.append(direction)
                directions = newDirections
                if len(directions) != 0:
                    self.currentDirection = random.choice(directions)
            else:
                targetx, targety = target.position

                match self.name:
                    case "Blinky": #Chase
                        self.pathfindToTarget(walls, ghostDoors, opposite, targetx, targety)
                    case "Pinky": #Intercept
                        match target.currentDirection:
                            case "up":
                                targetx -= 4 * tileSize
                                targety -= 4 * tileSize
                            case "down":
                                targety += 4 * tileSize
                            case "left":
                                targetx -= 4 * tileSize
                            case "right":
                                targetx += 4 * tileSize
                        self.pathfindToTarget(walls, ghostDoors, opposite, targetx, targety)
                    case "Inky": #Unpredictable
                        pivotx, pivoty = targetx, targety
                        match target.currentDirection:
                            case "up":
                                pivotx -= 2 * tileSize
                                pivoty -= 2 * tileSize
                            case "down":
                                pivoty += 2 * tileSize
                            case "left":
                                pivotx -= 2 * tileSize
                            case "right":
                                pivotx += 2 * tileSize
                        vx, vy = 0, 0
                        for ghost in ghosts:
                            if ghost.name == "Blinky":
                                vx = pivotx - ghost.position[0]
                                vy = pivoty - ghost.position[1]
                        targetx = pivotx + vx
                        targety = pivoty + vy
                        self.pathfindToTarget(walls, ghostDoors, opposite, targetx, targety)
                    case "Clyde": #Shy
                        if self.findDistance(self.position[0], self.position[1], targetx, targety) <= 8*tileSize:
                            targetx, targety = 0, height
                        self.pathfindToTarget(walls, ghostDoors, opposite, targetx, targety)
        
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
    
    def warp(self, warps):
        for w in warps:
            if pygame.Rect(w[0]-tileSize//2, w[1]-tileSize//2, tileSize, tileSize).colliderect(pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, self.size*2, self.size*2)):
                self.position = warps[warps.index(w)-1]

                if self.position[0] < width // 2:
                    self.position = (self.position[0] + tileSize, self.position[1])
                else:
                    self.position = (self.position[0] - tileSize, self.position[1])