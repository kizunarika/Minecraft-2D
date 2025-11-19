from settings import *
from block import Block


class Chunk:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy

        self.blocks = {0: {}, 1: {}, 2: {}}  # z: {(lx, ly): Block}

    def set_block(self, lx, ly, z, block):
        self.blocks[z][(lx, ly)] = block

    def get_block(self, lx, ly, z):
        return self.blocks.get(z, {}).get((lx, ly))

    def remove_block(self, lx, ly, z):
        if (lx, ly) in self.blocks.get(z, {}):
            del self.blocks[z][(lx, ly)]

    def draw(self, surface, offset, z):
        blocks = self.blocks.get(z, {})
        for block in blocks.values():
            block.draw(surface, offset)

    def generate_chunk(self):
        base_y = 3
        for lx in range(CHUNK_SIZE):
            for ly in range(CHUNK_SIZE):
                wx = self.cx * CHUNK_SIZE + lx
                wy = self.cy * CHUNK_SIZE + ly

                if wy == base_y:
                    self.set_block(lx, ly, 1, Block(
                        (wx * TILE_SIZE, wy * TILE_SIZE), "grass"))
                elif wy > base_y and wy <= base_y + 3:
                    self.set_block(lx, ly, 1, Block(
                        (wx * TILE_SIZE, wy * TILE_SIZE), "dirt"))
                elif wy > base_y + 3:
                    self.set_block(lx, ly, 1, Block(
                        (wx * TILE_SIZE, wy * TILE_SIZE), "stone"))
