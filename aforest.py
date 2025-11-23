import math

import noise
import pygame

# set up pygame
pygame.init()

# set up the window
screen_width, screen_height = 1280, 800
screen = pygame.display.set_mode((screen_width, screen_height))
# set up the noise surface
noise_width, noise_height = 1280, 800
noise_scale = 10
noise_width = int(screen_width / noise_scale)
noise_height = int(screen_height / noise_scale)
# noise_width, noise_height = round(1280 / 10), round(800 / 10)
noise_surface = pygame.Surface((noise_width, noise_height))
# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
colors = [(0, 128, 0), (0, 64, 0), (0, 32, 0)]
# set up the noise
octaves = 1
freq = 256 * octaves
# generate the noise
noise_map = [
    [
        noise.pnoise2(x / freq, y / freq, octaves, repeatx=3024, repeaty=3024)
        for x in range(screen_width)
    ]
    for y in range(screen_height)
]
# set up the clock
clock = pygame.time.Clock()
# set up the animation
frame = 0
# set up the noise surface cache
noise_surface_cache = []
# set up the noise surface cache index
noise_surface_cache_index = 0
# set up the noise surface cache size
noise_surface_cache_size = 120
# set up the noise surface cache
for i in range(noise_surface_cache_size):

    print(f"caching {i} of {noise_surface_cache_size}")
    # draw the background
    for y in range(noise_height):
        for x in range(noise_width):
            color = colors[2]
            if (
                noise_map[y * noise_scale][x * noise_scale]
                + math.sin(i * (3.14 / noise_surface_cache_size))
                > 0.2
            ):
                color = colors[1]
            elif (
                noise_map[y * noise_scale][x * noise_scale]
                + math.sin(i * (3.14 / noise_surface_cache_size))
                < 0.15
            ):
                color = colors[0]
            noise_surface.set_at((x, y), color)
    # cache the noise surface

    noise_surface_scaled = pygame.transform.scale(
        noise_surface, (screen_width, screen_height)
    )
    # noise_surface_scaled_pil = Image.frombytes(
    #     "RGB",
    #     (screen_width, screen_height),
    #     pygame.image.tostring(noise_surface_scaled, "RGB", False),
    # )

    # noise_surface_scaled_pil = noise_surface_scaled_pil.filter(
    #     ImageFilter.GaussianBlur(radius=20)
    # )
    # noise_surface_scaled = pygame.image.fromstring(
    #     noise_surface_scaled_pil.tobytes(), (screen_width, screen_height), "RGB"
    # )
    noise_surface_cache.append(noise_surface_scaled)

noise_surface_cache.extend([n for n in noise_surface_cache[::-1]])
# main loop
running = True
print("running")
while running:
    # keep loop running at the right speed
    clock.tick(60)
    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # increment the frame
    frame += 0.2
    if frame > noise_surface_cache_size - 1:
        frame = 0
    # draw the noise surface onto the screen
    screen.blit(noise_surface_cache[int(frame)], (0, 0))

    # display the fps on the screen
    pygame.display.set_caption(str(clock.get_fps()))
    # update the display
    pygame.display.flip()

pygame.quit()
