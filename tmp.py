import noise
import pygame

# Initialize pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([800, 600])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0, 0, 0))

    # Draw stars
    for i in range(2000):
        x = int(noise.pnoise1(i / 10.0, octaves=4) * 800)
        y = int(noise.pnoise1(i / 10.0 + 1000, octaves=4) * 600)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)

    # Draw the moon
    pygame.draw.circle(screen, (180, 180, 180), (400, 5600 - 200), 5000, 0)  # moon

    # Draw craters on the surface of the moon (masked by the shape of the moon)
    for i in range(20):
        x = int(noise.pnoise1(i / 10.0, octaves=4) * 800)
        y = int(noise.pnoise1(i / 10.0 + 1000, octaves=4) * 600)
        pygame.draw.circle(screen, (100, 100, 100), (x, y), 20, 0)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
