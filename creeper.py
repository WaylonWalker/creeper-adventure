from itertools import cycle, repeat
from pathlib import Path

import pygame
from more_itertools import flatten

from game import Game


class Creeper(Game):
    def __init__(self):
        super().__init__()
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 255, 247))
        self.x, self.y = [i / 2 for i in self.screen.get_size()]
        self.spot = pygame.image.load("assets/spotlight.png")
        self.darkness = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.light_power = 1.1
        self.creepers = cycle(
            flatten(
                [
                    repeat(pygame.image.load(img), 10)
                    for img in Path("assets/creeper/idle/").glob("*.png")
                ]
            )
        )
        self.creeper = pygame.image.load("assets/creeper/idle/1.png")

    def game(self):
        self.screen.blit(self.background, (0, 0))
        creeper = next(self.creepers)
        self.screen.blit(
            creeper,
            (self.x - creeper.get_size()[0] / 2, self.y - creeper.get_size()[1] / 2)
            # pygame.transform.scale(next(self.creepers), (96, 128)), (self.x, self.y)
        )
        self.darkness.fill((0, 0, 0))
        if self.light_power < 500:
            self.light_power = min(self.light_power ** 1.1, 500)
        self.darkness.blit(
            pygame.transform.smoothscale(
                self.spot, [self.light_power, self.light_power]
            ),
            (self.x - self.light_power / 2, self.y - self.light_power / 2),
        )
        self.screen.blit(
            self.darkness,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT,
        )
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= 10
        if keys[pygame.K_d]:
            self.x += 10


if __name__ == "__main__":
    creeper = Creeper()
    creeper.run()
