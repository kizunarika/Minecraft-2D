import pygame
from settings import *


def get_image(sheet, x, y, width, height):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(
        image, (image.width * TILE_SIZE // 16, image.height * TILE_SIZE // 16))
    return image


def blit_center(surf, img, x, y):
    rect = img.get_rect(center=(x, y))
    surf.blit(img, rect)


def rotate_image(image, pivot, angle, pivot_pos):
    """
    Xoay ảnh quanh pivot nội bộ (pivot nằm trong ảnh) và đặt pivot đó
    vào vị trí pivot_pos (tọa độ trên surface cha).

    Trả về:
        rotated_image, rotated_rect

    Tham số:
    - image: pygame.Surface  → ảnh gốc
    - pivot: (x, y)          → tọa độ pivot trong ảnh (tính từ góc trái trên)
    - angle: float           → góc xoay (độ, ngược chiều kim đồng hồ)
    - pivot_pos: (x, y)      → tọa độ nơi pivot cần nằm sau khi xoay (trên màn hình)
    """
    # Vector hóa để dễ tính
    pivot = vec(pivot)
    pivot_pos = vec(pivot_pos)

    # Lấy tâm ảnh gốc
    rect = image.get_rect(topleft=(0, 0))
    center = vec(rect.center)

    # Vector từ pivot → center
    offset = center - pivot

    # Xoay ảnh
    rotated_image = pygame.transform.rotate(image, angle)

    # Xoay vector offset cùng góc
    rotated_offset = offset.rotate(angle)

    # Tính tâm mới của ảnh xoay sao cho pivot nằm đúng vị trí pivot_pos
    new_center = pivot_pos + rotated_offset

    # Tạo rect mới
    rotated_rect = rotated_image.get_rect(center=new_center)

    return rotated_image, rotated_rect
