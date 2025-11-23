import math

from noise import pnoise2
import pygame

# Initialize pygame
pygame.init()

base = 0
persistence = 0.4
lacunarity = 2.0
more_x = 0
# Set up the drawing window
screen = pygame.display.set_mode([800, 600])


def S():
    i = 0
    while True:
        i += 0.1
        yield math.sin(i)


s = S()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    m = next(s)
    # Generate Perlin noise
    for x in range(800):
        for y in range(600):
            noise = pnoise2(
                x / 10,
                y / 10,
                octaves=4,
                persistence=persistence + m / 10,
                lacunarity=lacunarity,
                repeatx=1024,
                repeaty=1024,
                base=base,
            )
            if noise > 0.2:
                pygame.draw.rect(screen, (0, 255, 0), (x, y, 1, 1))
            elif noise > 0:
                pygame.draw.rect(screen, (0, 128, 0), (x, y, 1, 1))
            else:
                pygame.draw.rect(screen, (0, 64, 0), (x, y, 1, 1))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
