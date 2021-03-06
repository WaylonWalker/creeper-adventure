import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(__file__)

        self.screen_size = (854, 480)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        self.running = True
        self.surfs = []

    def should_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def game(self):
        ...

    def reset_screen(self):
        self.screen.fill((0, 0, 0))

    def run(self):
        while self.running:
            self.should_quit()
            self.reset_screen()
            self.game()
            for surf in self.surfs:
                pygame.blit(surf)
            pygame.display.update()
            self.clock.tick(30)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
