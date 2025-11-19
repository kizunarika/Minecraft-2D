from settings import *
from block_data import BLOCKS


class Block:
    def __init__(self, pos, name):
        data = BLOCKS[name]
        self.name = name
        self.image = data["texture"]
        self.rect = self.image.get_rect(topleft=pos)
        self.drop = data["drops"]

        self.hardness = data["hardness"]

    def draw(self, surface, offset):
        surface.blit(self.image, self.rect.topleft - offset)
