from player import Player
from settings import *
from block import Block
from world import World
from mine import Mine
from block_data import BLOCKS
from item_data import Items


class Game:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.load_image()
        self.world = World()
        self.player = Player((0, 0))
        self.offset = vec(0, 0)
        self.mine = Mine(self.world)

        self.pointer_surf_white = pygame.transform.scale(pygame.image.load(
            join('data', 'graphics', 'ui', 'pointer_white.png')).convert_alpha(), (TILE_SIZE, TILE_SIZE))

    def load_image(self):
        for block_data in BLOCKS.values():
            texture_path = block_data.get("texture")
            if texture_path:
                block_data["texture"] = pygame.transform.scale(
                    pygame.image.load(join('data', 'graphics', 'blocks', texture_path)).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        for item_data in Items.values():
            texture_path = item_data.get("texture")
            if texture_path:
                item_data["texture"] = pygame.image.load(
                    join('data', 'graphics', 'blocks', texture_path)).convert_alpha()

    def draw(self):
        self.display_surface.fill((0, 0, 0))

        self.world.draw(self.display_surface, self.offset, z=0)
        for item in self.world.dropped_items:
            item.draw(self.display_surface, self.offset)
        self.draw_overlay()
        self.world.draw(self.display_surface, self.offset, z=1)
        self.player.draw(self.display_surface, self.offset)
        self.world.draw(self.display_surface, self.offset, z=2)

        self.mine.draw_crack(self.display_surface, self.offset)
        self.draw_pointer()

    def draw_overlay(self):
        overlay = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 128))
        self.display_surface.blit(overlay, (0, 0))

    def draw_pointer(self):
        cell_x, cell_y = self.mouse_to_block_index(
            pygame.mouse.get_pos(), self.offset)
        draw_x = cell_x * TILE_SIZE - self.offset.x
        draw_y = cell_y * TILE_SIZE - self.offset.y

        self.display_surface.blit(self.pointer_surf_white, (draw_x, draw_y))

    def mouse_to_block_index(self, mouse_pos, offset):
        world_x = mouse_pos[0] + offset.x
        world_y = mouse_pos[1] + offset.y
        block_x = int(world_x // TILE_SIZE)
        block_y = int(world_y // TILE_SIZE)
        return block_x, block_y

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = self.mouse_to_block_index(
                        pygame.mouse.get_pos(), self.offset)
                    self.mine.start_mining(x, y, z=1)
                elif event.button == 3:
                    x, y = self.mouse_to_block_index(
                        pygame.mouse.get_pos(), self.offset)
                    if self.world.is_placeable(x, y, z=1, player_rect=self.player.rect):
                        Item = self.player.inventory.slots[self.player.selected_item]
                        if Item:
                            block_name = Item[0].name
                            block = Block(
                                (x * TILE_SIZE, y * TILE_SIZE), block_name)
                            self.world.set_block(x, y, 1, block)
                            self.player.inventory.remove_item(
                                self.player.selected_item)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mine.stop_mining()

    def update(self, dt):
        self.player.update(dt, self.world)
        self.offset = vec(self.player.rect.centerx - WINDOW_WIDTH / 2,
                          self.player.rect.centery - WINDOW_HEIGHT / 2)
        self.event()
        self.mine.update()
        self.world.dropped_items = [
            item for item in self.world.dropped_items
            if not item.update(dt, self.player, self.world)
        ]
        self.draw()
