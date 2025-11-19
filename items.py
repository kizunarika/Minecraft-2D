from settings import *
from item_data import Items
from random import uniform
from time import time
from math import sin


class Item:
    def __init__(self, name, max_stack=64):
        self.name = name
        self.texture = Items[name]['texture']
        self.max_stack = max_stack


class DroppedItem:
    def __init__(self, item, pos):
        self.item = item
        self.pos = vec(pos)
        self.vel = vec(uniform(-150, 150), uniform(-400, -250))
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.rect.center = self.pos

        self.bounce_damping = 0.4
        self.grounded = False

        self.spawn_time = time()

    def update(self, dt, player, world):
        # gravity
        if not self.grounded:
            self.vel.y += GRAVITY * dt

        # move
        self.pos += self.vel * dt
        self.rect.center = self.pos

        # collision
        self.check_collision(world)

        # pickup
        if self.rect.colliderect(player.rect):
            player.inventory.add_item(self.item)
            return True
        return False

    def check_collision(self, world):
        # --- vertical collision (ground) ---
        block_below = world.get_block(
            int(self.rect.centerx // TILE_SIZE),
            int(self.rect.bottom // TILE_SIZE),
            1
        )
        if block_below:
            if self.vel.y > 0:  # falling
                self.rect.bottom = block_below.rect.top
                self.pos.y = self.rect.centery
                self.vel.y *= -self.bounce_damping

                # stop if very slow
                if abs(self.vel.y) < 40:
                    self.vel.y = 0
                    self.grounded = True
        else:
            self.grounded = False

        # --- horizontal collision (walls) ---
        left_block = world.get_block(
            int(self.rect.left // TILE_SIZE),
            int(self.rect.centery // TILE_SIZE),
            1
        )
        right_block = world.get_block(
            int(self.rect.right // TILE_SIZE),
            int(self.rect.centery // TILE_SIZE),
            1
        )

        if left_block and self.vel.x < 0:
            self.rect.left = left_block.rect.right
            self.pos.x = self.rect.centerx
            self.vel.x *= -self.bounce_damping

        elif right_block and self.vel.x > 0:
            self.rect.right = right_block.rect.left
            self.pos.x = self.rect.centerx
            self.vel.x *= -self.bounce_damping

        # friction
        if self.grounded:
            self.vel.x *= 0.9
            if abs(self.vel.x) < 10:
                self.vel.x = 0

    def draw(self, surface, offset):
        # bob effect
        t = time() - self.spawn_time
        bob = sin(t * 6) * 2

        center_pos = (
            self.rect.centerx - offset.x,
            self.rect.centery - offset.y + bob
        )

        rect = self.item.texture.get_rect(center=center_pos)
        surface.blit(self.item.texture, rect.topleft)


class Inventory:
    def __init__(self, size=9):
        self.slots = [None] * size  # (Item, count)

    def add_item(self, item):
        # stack
        for i, slot in enumerate(self.slots):
            if slot and slot[0].name == item.name and slot[1] < slot[0].max_stack:
                self.slots[i] = (slot[0], slot[1] + 1)
                return True
        # new slot
        for i, slot in enumerate(self.slots):
            if slot is None:
                self.slots[i] = (item, 1)
                return True
        return False  # full

    def remove_item(self, index):
        if self.slots[index]:
            item, count = self.slots[index]
            if count > 1:
                self.slots[index] = (item, count - 1)
            else:
                self.slots[index] = None

    def print_inventory(self):
        for i, slot in enumerate(self.slots):
            if slot:
                print(f"Slot {i}: {slot[0].name} x{slot[1]}")
