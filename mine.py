from settings import *
from items import Item, DroppedItem


class Mine:
    def __init__(self, world):
        self.world = world
        self.target_block = None
        self.start_time = None
        self.progress = 0
        self.mining = False
        self.crack_sprites = []
        for i in range(10):
            img = pygame.image.load(
                join('data', 'graphics', 'effects', f'destroy_stage_{i}.png')).convert_alpha()
            self.crack_sprites.append(
                pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)))

    def start_mining(self, x, y, z=1):
        block = self.world.get_block(x, y, z)
        if block:
            self.target_block = block
            self.start_time = pygame.time.get_ticks()
            self.progress = 0
            self.mining = True

    def update(self):
        if self.mining and self.target_block:
            elapsed = pygame.time.get_ticks() - self.start_time
            if elapsed >= self.target_block.hardness:
                self.break_block()
            else:
                self.progress = elapsed / self.target_block.hardness

    def draw_crack(self, surface, offset):
        if self.mining and self.target_block:
            crack_index = min(int(self.progress * 10), 9)
            crack_image = self.crack_sprites[crack_index]
            pos = self.target_block.rect.topleft - offset
            surface.blit(crack_image, pos)

    def break_block(self):
        if self.target_block:
            # drop item
            item = Item(self.target_block.drop)
            dropped_item = DroppedItem(item, (
                self.target_block.rect.centerx,
                self.target_block.rect.centery
            ))

            self.world.add_dropped_item(dropped_item)

            self.world.remove_block(self.target_block.rect.x // TILE_SIZE,
                                    self.target_block.rect.y // TILE_SIZE, 1)
            self.target_block = None
            self.mining = False

    def stop_mining(self):
        self.mining = False
        self.target_block = None
