import pygame
import math
from settings import *
from support import rotate_image


class BaseAnimation:
    def __init__(self, player):
        self.player = player

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def rotate_image(self, image, pivot, angle, pivot_pos):
        pivot = pygame.Vector2(pivot)
        pivot_pos = pygame.Vector2(pivot_pos)
        rect = image.get_rect(topleft=(0, 0))
        center = pygame.Vector2(rect.center)
        offset = center - pivot
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_offset = offset.rotate(angle)
        new_center = pivot_pos + rotated_offset
        rotated_rect = rotated_image.get_rect(center=new_center)
        return rotated_image, rotated_rect


class RunAnimation(BaseAnimation):
    def __init__(self, player):
        super().__init__(player)
        self.walk_speed = 8.0
        self.amplitude = 30  # góc xoay tối đa

    def update(self, dt):
        super().update(dt)
        self.cycle = self.time * self.walk_speed

        # tay & chân ngược pha
        self.arm_angle = math.sin(self.cycle) * self.amplitude
        self.leg_angle = math.sin(self.cycle + math.pi) * self.amplitude
        self.body_offset_y = math.sin(self.cycle * 2) * 1.5
        self.head_tilt = math.sin(self.cycle) * 3

    def draw(self, surface):
        f = self.player.direction_face
        surf = self.player.player_surf
        surf.fill((0, 0, 0, 0))

        img = self.player.images
        scale = self.player.SCALING_FACTOR if hasattr(
            self.player, "SCALING_FACTOR") else 1
        cx, cy = 8 * scale, 15 * scale

        # --- Body ---
        body = img["body"][f]
        surf.blit(body, body.get_rect(center=(cx, cy + self.body_offset_y)))

        # --- Arms ---
        pivot_arm = (2 * scale, 2 * scale)
        left_arm = img["left_arm"][f]
        right_arm = img["right_arm"][f]

        rotated, rect = rotate_image(
            left_arm, pivot_arm, self.arm_angle, (cx - 6, cy))
        surf.blit(rotated, rect)

        rotated, rect = rotate_image(
            right_arm, pivot_arm, -self.arm_angle, (cx + 6, cy))
        surf.blit(rotated, rect)

        # --- Legs ---
        pivot_leg = (2 * scale, 2 * scale)
        left_leg = img["left_leg"][f]
        right_leg = img["right_leg"][f]

        rotated, rect = rotate_image(
            left_leg, pivot_leg, self.leg_angle, (cx - 3, cy + 10))
        surf.blit(rotated, rect)

        rotated, rect = rotate_image(
            right_leg, pivot_leg, -self.leg_angle, (cx + 3, cy + 10))
        surf.blit(rotated, rect)

        # --- Head ---
        head = img["head"][f]
        rotated, rect = rotate_image(
            head, (4 * scale, 4 * scale), self.head_tilt, (cx, 5 * scale))
        surf.blit(rotated, rect)
