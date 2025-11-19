import pygame
import sys
from pygame.math import Vector2 as vec
from os.path import join


WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
SCALING_FACTOR = TILE_SIZE // 16
ANIMATION_SPEED = 6
GRAVITY = 2000

CHUNK_SIZE = 16  # in blocks
