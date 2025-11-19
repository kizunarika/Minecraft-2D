from settings import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Minecraft 2D')
        self.clock = pygame.time.Clock()

        self.game = Game()

    def run(self):
        while True:
            dt = self.clock.tick() / 1000

            self.game.update(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Main()
    game.run()
