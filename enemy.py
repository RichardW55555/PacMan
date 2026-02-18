import pygame
import os
from character import *
from constants import *

class Enemy(Character):
    def __init__(self, startCol, startRow, color):
        super().__init__(startCol, startRow)
        self.size = 10
        self.speed = tileSize
        self.raw_img = pygame.image.load(os.path.join("Assets", f"{color} Ghost.png"))