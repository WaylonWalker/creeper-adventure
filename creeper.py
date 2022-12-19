import random
from itertools import cycle, repeat
from pathlib import Path

import pygame
from more_itertools import flatten

from game import Game


class LightSource:
    def __init__(self, game: Game, surf, img, center):
        self.surf = surf
        self.game = game
        self.img = img
        self.center = center
        self.sx, self.sy = center
        self.spot = pygame.image.load("assets/spotlight.png")


class Leaf:
    def __init__(self, game: Game, surf, img, center):
        self.surf = surf
        self.game = game
        self.img = img
        self.center = center
        self.sx, self.sy = center
        self.restart()

    def restart(self):
        self.r = random.randint(0, 360)
        self.x, self.y = [int(i) + random.randint(-8, 8) for i in self.center]

    def draw(self):
        self.surf.blit(
            pygame.transform.rotate(self.img, self.r), (int(self.x), int(self.y))
        )
        # pygame.draw.circle(self.surf, (255, 0, 0), self.center, 16)
        # pygame.draw.circle(self.surf, (255, 255, 0), (self.sx, self.sy + 45), 5)

        if self.y < self.sy + 40:
            self.y += random.randint(0, 5) / 4
            self.x += random.randint(-15, 5) / 10
            self.r += random.randint(-10, 10)
        elif self.y < self.sy + 45:
            self.y += random.randint(-2, 5) / 10
            self.x += random.randint(-18, 2) / 10
            self.r += random.randint(-10, 25)
        else:
            self.restart()
        if self.x > self.sx + 100:
            self.restart()


class Bee:
    def __init__(self):
        self.bee = pygame.image.load("assets/bee/idle/1.png")
        self.x = 0
        self.y = 0

    def draw(self, screen, x, y):
        self.x += random.randint(-2, 2)
        self.y += random.randint(-2, 2)
        screen.blit(
            self.bee,
            (
                x + self.x - self.bee.get_size()[0] / 2,
                y + self.y - self.bee.get_size()[1] / 2,
            ),
        )


class Creeper(Game):
    def __init__(self):
        super().__init__()
        self.background = pygame.Surface(self.screen.get_size())
        self.foreground = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 255, 247))
        self.x, self.y = [i / 2 for i in self.screen.get_size()]
        self.spot = pygame.image.load("assets/spotlight.png")
        self.darkness = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.light_power = 1.1
        self.leaf = pygame.transform.scale(
            pygame.image.load("assets/leaf.png"), (4, 4)
        ).convert_alpha()
        self.creepers = cycle(
            flatten(
                [
                    repeat(pygame.image.load(img), 10)
                    for img in Path("assets/creeper/idle/").glob("*.png")
                ]
            )
        )
        self.trees = [
            pygame.image.load(img) for img in Path("assets/oak_trees/").glob("*.png")
        ]
        self.creeper = pygame.image.load("assets/creeper/idle/1.png")
        self.bee = Bee()
        x = 0
        self.leafs = []
        for i in range(10):
            x += random.randint(10, 110)
            y = random.randint(180, 200)
            self.leafs.extend(
                [Leaf(self, self.screen, self.leaf, (x + 25, y + 25)) for i in range(2)]
            )
            scale = random.randint(42, 86)
            self.background.blit(
                pygame.transform.flip(
                    pygame.transform.scale(random.choice(self.trees), (scale, scale)),
                    random.randint(0, 1),
                    False,
                ),
                (x, y),
            )
        for i in range(10):
            x += random.randint(10, 110)
            y = random.randint(180, 200)
            scale = random.randint(42, 86)
            self.foreground.blit(
                pygame.transform.flip(
                    pygame.transform.scale(random.choice(self.trees), (scale, scale)),
                    random.randint(0, 1),
                    False,
                ),
                (x, y),
            )

    def game(self):
        self.screen.blit(self.background, (0, 0))
        creeper = next(self.creepers)
        self.screen.blit(
            creeper,
            (self.x - creeper.get_size()[0] / 2, self.y - creeper.get_size()[1] / 2)
            # pygame.transform.scale(next(self.creepers), (96, 128)), (self.x, self.y)
        )
        self.bee.draw(self.screen, self.x, self.y)
        for leaf in self.leafs:
            leaf.draw()
        # self.screen.blit(self.foreground, (0, 0))
        self.darkness.fill((25, 25, 25))
        if self.light_power < 500:
            self.light_power = min(self.light_power**1.1, 500)
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
