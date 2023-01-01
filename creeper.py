import random
from itertools import cycle, repeat
from pathlib import Path

import pygame
from more_itertools import flatten

from game import Game


class MouseSprite:
    def __init__(self, surf):
        self.surf = surf
        self.image = pygame.image.load("assets/spotlight.png")

    @property
    def mouse_pos(self):
        return [i - 2 for i in pygame.mouse.get_pos()]

    @property
    def rect(self):
        return pygame.Rect(self.mouse_pos, (4, 4))

    def draw(self):
        pygame.draw.rect(self.surf, (255, 0, 0), self.rect)


class TreeSprite:
    def __init__(self, tree, x, y, scale, flip, surf):
        self.image = tree
        self.health = 100
        self.x = x
        self.y = y
        self.scale = scale
        self.flip = flip
        self.surf = surf
        self.leafs = [Leaf(self, self.surf, (x + 25, y + 25)) for i in range(2)]
        self.shaking = 0

    def shake(self):
        if self.shaking == 0:
            self.shaking = 10
        self.leafs.extend(
            [
                Leaf(
                    self,
                    self.surf,
                    (
                        self.x + 25 + random.randint(-10, 10),
                        self.y + 25 + random.randint(-10, 10),
                    ),
                    lifespan=1,
                )
                for i in range(2)
            ]
        )

    @property
    def rotate(self):
        if self.shaking == 0:
            return 0
        self.shaking -= 1
        return random.randint(-15, 15)

    @property
    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.scale,
            self.scale,
        )

    def draw(self):
        if self.health > 0:
            self.surf.blit(
                pygame.transform.rotate(
                    pygame.transform.flip(
                        pygame.transform.scale(self.image, (self.scale, self.scale)),
                        self.flip,
                        False,
                    ),
                    self.rotate,
                ),
                (self.x, self.y),
            )
            for leaf in self.leafs:
                leaf.draw()


class HotBar:
    def __init__(self, game: Game, surf, num=8):
        self.ui = surf
        self.game = game
        self.items = [
            HotBarItem(game=self, surf=self.ui, pos=pos) for pos in range(num)
        ]
        self.items[0].selected = True

    @property
    def selected(self):
        return [bar for bar in self.items if bar.selected][0]

    def next(self, step):
        cur_idx = self.items.index(self.selected)
        next_idx = cur_idx + step
        self.items[cur_idx].selected = False
        if next_idx >= len(self.items):
            self.items[0].selected = True
        elif next_idx < 0:
            self.items[-1].selected = True
        else:
            self.items[next_idx].selected = True


class HotBarItem:
    def __init__(self, game: Game, surf, pos=0):
        self.ui = surf
        self.game = game
        self.surf = pygame.Surface((16, 16)).convert_alpha()
        self.pos = pos
        self.selected = False
        self.surf.fill((0, 0, 0))

    def draw(self):
        if self.selected:
            self.surf.fill((100, 100, 100))
        else:
            self.surf.fill((0, 0, 0))
        self.ui.blit(self.surf, (self.pos * 24 + 4, 4))


class LightSource:
    def __init__(self, game: Game, surf, img, center):
        self.surf = surf
        self.game = game
        self.img = img
        self.center = center
        self.sx, self.sy = center
        self.spot = pygame.image.load("assets/spotlight.png")


class Leaf:
    def __init__(self, game: Game, surf, center, lifespan=None):
        self.surf = surf
        self.game = game
        self.center = center
        self.sx, self.sy = center
        self.img = pygame.transform.scale(
            pygame.image.load("assets/leaf.png"), (4, 4)
        ).convert_alpha()
        self.lifespan = lifespan
        self.r = random.randint(0, 360)
        self.x, self.y = [int(i) + random.randint(-8, 8) for i in self.center]
        self.restart()

    def restart(self):
        if self.lifespan is not None:
            self.lifespan -= 1
        if self.lifespan is None or self.lifespan > 0:
            self.r = random.randint(0, 360)
            self.x, self.y = [int(i) + random.randint(-8, 8) for i in self.center]

    def draw(self):
        self.surf.blit(
            pygame.transform.rotate(self.img, self.r), (int(self.x), int(self.y))
        )

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
        self.day_len = 1000 * 60
        self.background = pygame.Surface(self.screen.get_size())
        self.foreground = pygame.Surface(self.screen.get_size())
        self.ui = pygame.Surface((24 * 8, 24), pygame.SRCALPHA, 32).convert_alpha()
        self.ui.fill((50, 50, 50))
        self.darkness = pygame.Surface(self.screen.get_size()).convert_alpha()

        self.background.fill((0, 255, 247))
        self.x, self.y = [i / 2 for i in self.screen.get_size()]
        self.spot = pygame.image.load("assets/spotlight.png")
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
        self.tree_imgs = [
            pygame.image.load(img) for img in Path("assets/oak_trees/").glob("*.png")
        ]
        self.creeper = pygame.image.load("assets/creeper/idle/1.png")
        self.bee = Bee()
        x = 0
        self.hotbar = HotBar(game=self, surf=self.ui)
        self.leafs = []
        self.trees = []
        for i in range(10):
            x += random.randint(10, 110)
            y = random.randint(180, 200)

            scale = random.randint(42, 86)
            self.trees.append(
                TreeSprite(
                    tree=random.choice(self.tree_imgs),
                    x=x,
                    y=y,
                    scale=scale,
                    flip=random.randint(0, 1),
                    surf=self.background,
                )
            )
        self.joysticks = {}

    def attack(self):

        collisions = self.mouse_box.rect.collidedictall(
            {tree: tree.rect for tree in self.trees}
        )
        for collision in collisions:
            tree = collision[0]
            tree.health -= 10
            tree.hit = True
            tree.shake()

    def game(self):
        creeper = next(self.creepers)
        self.mouse_box = MouseSprite(self.screen)
        self.screen.blit(self.background, (0, 0))
        self.background.fill((0, 255, 247))
        for tree in self.trees:
            tree.draw()

        self.screen.blit(
            creeper,
            (self.x - creeper.get_size()[0] / 2, self.y - creeper.get_size()[1] / 2),
        )
        self.bee.draw(self.screen, self.x, self.y)
        for leaf in self.leafs:
            leaf.draw()

        light_level = pygame.time.get_ticks() % self.day_len
        light_level = abs(light_level * (255 * 2 / self.day_len) - 255)

        self.darkness.fill((light_level, light_level, light_level))
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
        for hot_bar_item in self.hotbar.items:
            hot_bar_item.draw()

        y = self.screen.get_size()[1] - 24 - 4
        x = self.screen.get_size()[0] / 2 - (24 * 8 - 8) / 2
        self.screen.blit(
            self.ui,
            (x, y),
        )

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= 10
        if keys[pygame.K_d]:
            self.x += 10
        if keys[pygame.K_k]:
            self.hotbar.next(1)
        if keys[pygame.K_j]:
            self.hotbar.next(-1)
        for event in self.events:
            if event.type == pygame.MOUSEWHEEL:
                self.hotbar.next(event.y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.attack()

            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")
            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        print(self.joysticks)
        for joystick in self.joysticks.values():

            if joystick.get_button(4) and self.hotbar_debounce:
                self.hotbar.next(-1)
                self.hotbar_debounce = 0

            if joystick.get_button(5) and self.hotbar_debounce:
                self.hotbar.next(1)
                self.hotbar_debounce = 0

            if not joystick.get_button(4) and not joystick.get_button(5):
                self.hotbar_debounce = 1

            hats = joystick.get_numhats()
            print("numhats", hats)
            for i in range(hats):
                hat = joystick.get_hat(i)
                if hat[0] == 1:
                    self.x += 10
                if hat[0] == -1:
                    self.x -= 10

        self.mouse_box.draw()


if __name__ == "__main__":
    creeper = Creeper()
    creeper.run()
