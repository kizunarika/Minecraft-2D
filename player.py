import pygame
from os.path import join
from settings import *
from support import get_image, blit_center
from items import Inventory
from player_animation import PlayerAnimation

vec = pygame.math.Vector2


class Player:
    def __init__(self, pos):
        # load spritesheet
        self.spritesheet = pygame.image.load(
            join('data', 'graphics', 'entities', 'steve.png')
        ).convert_alpha()

        self.inventory = Inventory()
        self.selected_item = 0

        self.images = {
            "head": [
                get_image(self.spritesheet, 8, 8, 8, 8),    # front
                get_image(self.spritesheet, 16, 8, 8, 8),   # left
                get_image(self.spritesheet, 24, 8, 8, 8),   # back
                get_image(self.spritesheet, 0, 8, 8, 8),    # right
            ],
            "body": [
                get_image(self.spritesheet, 20, 20, 8, 12),
                get_image(self.spritesheet, 16, 20, 4, 12),
                get_image(self.spritesheet, 32, 20, 8, 12),
                get_image(self.spritesheet, 28, 20, 4, 12),
            ],
            "right_arm": [
                get_image(self.spritesheet, 44, 20, 4, 12),
                get_image(self.spritesheet, 48, 20, 4, 12),
                get_image(self.spritesheet, 52, 20, 4, 12),
                get_image(self.spritesheet, 40, 20, 4, 12),
            ],
            "left_arm": [
                get_image(self.spritesheet, 36, 52, 4, 12),
                get_image(self.spritesheet, 40, 52, 4, 12),
                get_image(self.spritesheet, 44, 52, 4, 12),
                get_image(self.spritesheet, 32, 52, 4, 12),
            ],
            "right_leg": [
                get_image(self.spritesheet, 4, 20, 4, 12),
                get_image(self.spritesheet, 0, 20, 4, 12),
                get_image(self.spritesheet, 12, 20, 4, 12),
                get_image(self.spritesheet, 8, 20, 4, 12),
            ],
            "left_leg": [
                get_image(self.spritesheet, 20, 52, 4, 12),
                get_image(self.spritesheet, 24, 52, 4, 12),
                get_image(self.spritesheet, 28, 52, 4, 12),
                get_image(self.spritesheet, 16, 52, 4, 12),
            ]
        }

        # movement
        self.direction = vec(0, 1)
        self.velocity = vec(0, 0)
        self.speed = 200
        self.multiplier_speed_air = 0.8
        self.multiplier_speed_run = 1.8
        self.jump_velocity = -600
        self.gravity = 2000

        # model
        self.animation = PlayerAnimation(self)
        self.rect = pygame.Rect(
            pos, (12 * SCALING_FACTOR, 30 * SCALING_FACTOR))
        self.direction_face = 0   # 0: front, 1: left, 2: back, 3: right
        self.player_surf = pygame.Surface(
            (16 * SCALING_FACTOR, 32 * SCALING_FACTOR), pygame.SRCALPHA)

        # status
        self.status = {
            "jump": False,
            "on_floor": False,
            "run": False,
        }

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0

        if keys[pygame.K_d]:
            self.direction_face, self.direction.x = 3, 1
        elif keys[pygame.K_a]:
            self.direction_face, self.direction.x = 1, -1
        elif keys[pygame.K_w]:
            self.direction_face = 2
        elif keys[pygame.K_s]:
            self.direction_face = 0

        for i in range(1, 10):
            if keys[getattr(pygame, f'K_{i}')]:
                self.selected_item = i - 1
                break

        self.status["run"] = keys[pygame.K_LCTRL]
        self.status["jump"] = keys[pygame.K_SPACE]

    def move(self, dt, world):
        if self.status['on_floor']:
            speed = self.speed * \
                (self.multiplier_speed_run if self.status['run'] else 1)
        else:
            speed = self.speed * self.multiplier_speed_air

        self.velocity.x = self.direction.x * speed

        if self.status['jump'] and self.status['on_floor']:
            self.velocity.y = self.jump_velocity
            self.status['jump'] = False
            self.status['on_floor'] = False

        self.velocity.y += self.gravity * dt

        dx, dy = self.velocity.x * dt, self.velocity.y * dt

        # horizontal
        if not self.check_collision(dx, 0, world):
            self.rect.x += dx
        # vertical
        if not self.check_collision(0, dy, world):
            self.rect.y += dy
            self.status["on_floor"] = False

    def check_collision(self, dx, dy, world):
        future_rect = self.rect.copy()
        future_rect.x += dx
        future_rect.y += dy

        left = future_rect.left // TILE_SIZE
        right = future_rect.right // TILE_SIZE
        top = future_rect.top // TILE_SIZE
        bottom = future_rect.bottom // TILE_SIZE

        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                block = world.get_block(tx, ty, 1)
                if block and block.rect.colliderect(future_rect):
                    if dy > 0:
                        self.status["on_floor"] = True
                        self.velocity.y = 0
                        self.rect.bottom = block.rect.top
                    elif dy < 0:
                        self.velocity.y = 0
                        self.rect.top = block.rect.bottom
                    return True
        return False

    def draw(self, surface, offset):
        self.player_surf.fill((0, 0, 0, 0))
        self.animation.draw(self.player_surf)

        blit_center(
            surface,
            self.player_surf,
            self.rect.centerx - offset.x,
            self.rect.centery - offset.y - SCALING_FACTOR
        )

    def update(self, dt, world):
        self.input()
        self.move(dt, world)
        self.animation.update(dt)
