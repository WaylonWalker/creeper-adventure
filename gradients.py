from noise import pnoise2
import pygame
import random

# Initialize pygame
pygame.init()

# Set the size of the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Create a list of 3 random blues
blues = []
for i in range(3):
    blues.append(
        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    )

# Create a perlin noise surface
noise_surface = pygame.Surface((width, height))
for x in range(width):
    for y in range(height):
        # Calculate the perlin noise value
        noise_value = pnoise2(x / 100, y / 100)
        # Map the noise value to a color
        color_index = int(noise_value * (len(blues) - 1))
        color = blues[color_index]
        # Set the color of the pixel
        noise_surface.set_at((x, y), color)

# Blit the noise surface to the screen
screen.blit(noise_surface, (0, 0))

# Update the display
pygame.display.flip()

# Keep the window open until it is closed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
