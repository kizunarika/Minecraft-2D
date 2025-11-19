from settings import *
from chunk import Chunk
from math import floor


class World:
    def __init__(self):
        self.chunks = {}
        self.dropped_items = []

# ----------------------- block management ----------------------- #

    def get_chunk(self, x, y, create=False):
        cx = x // CHUNK_SIZE
        cy = y // CHUNK_SIZE
        if (cx, cy) not in self.chunks:
            if create:
                self.chunks[(cx, cy)] = Chunk(cx, cy)
            else:
                return None
        return self.chunks[(cx, cy)]

    def set_block(self, x, y, z, block):
        cx, cy = x // CHUNK_SIZE, y // CHUNK_SIZE
        lx, ly = x % CHUNK_SIZE, y % CHUNK_SIZE
        chunk = self.get_chunk(x, y, create=True)
        chunk.set_block(lx, ly, z, block)

    def get_block(self, x, y, z):
        chunk = self.get_chunk(x, y, create=False)
        if not chunk:
            return None
        lx, ly = x % CHUNK_SIZE, y % CHUNK_SIZE
        return chunk.get_block(lx, ly, z)

    def remove_block(self, x, y, z):
        chunk = self.get_chunk(x, y, create=False)
        if not chunk:
            return
        lx, ly = x % CHUNK_SIZE, y % CHUNK_SIZE
        chunk.remove_block(lx, ly, z)

    def is_placeable(self, x, y, z=1, player_rect=None):
        if self.get_block(x, y, z):
            return False

        neighbors = [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z - 1),  # block bên dưới
            (x, y, z + 1)   # block bên trên
        ]

        has_support = False
        for nx, ny, nz in neighbors:
            if self.get_block(nx, ny, nz):
                has_support = True
                break

        if not has_support:
            return False

        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if player_rect.colliderect(rect):
            return False

        return True

    def draw(self, surface, offset, z):
        start_block_x = floor(offset.x / TILE_SIZE)
        start_block_y = floor(offset.y / TILE_SIZE)
        end_block_x = floor((offset.x + WINDOW_WIDTH - 1) / TILE_SIZE)
        end_block_y = floor((offset.y + WINDOW_HEIGHT - 1) / TILE_SIZE)

        start_chunk_x = floor(start_block_x / CHUNK_SIZE)
        start_chunk_y = floor(start_block_y / CHUNK_SIZE)
        end_chunk_x = floor(end_block_x / CHUNK_SIZE)
        end_chunk_y = floor(end_block_y / CHUNK_SIZE)

        for cx in range(start_chunk_x-1, end_chunk_x + 2):
            for cy in range(start_chunk_y-1, end_chunk_y + 2):
                chunk = self.chunks.get((cx, cy))
                if not chunk:  # create chunk if not exist
                    chunk = Chunk(cx, cy)
                    chunk.generate_chunk()
                    self.chunks[(cx, cy)] = chunk
                chunk.draw(surface, offset, z)

        for item in self.dropped_items:
            item.draw(surface, offset)

# ----------------------- dropped items ----------------------- #

    def add_dropped_item(self, item):
        self.dropped_items.append(item)

    def remove_dropped_item(self, i):
        self.dropped_items.pop(i)
