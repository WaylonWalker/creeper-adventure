import pygame

# Initialize Pygame
pygame.init()

EVENTS = []
# Set screen size
screen = pygame.display.set_mode((800, 600))

# Set title
pygame.display.set_caption("My RPG Game")

# Load font
font = pygame.font.Font(None, 30)

# Define button class
class Button:
    def __init__(self, text, x, y, w, h, on_click=lambda: ...):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.on_click = on_click

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.w, self.h))
        label = font.render(self.text, True, (0, 0, 0))
        label_rect = label.get_rect()
        label_rect.center = (self.x + self.w / 2, self.y + self.h / 2)
        surface.blit(label, label_rect)
        for event in EVENTS:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_clicked(event.pos):
                    self.on_click()
                # elif quit_button.is_clicked(event.pos):
                #     running = False
        # if self.is_clicked:
        #     self.on_click()

    def is_clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False


# Create buttons
start_button = Button(
    "Start Game", 300, 300, 200, 50, lambda: print("start this thing")
)
running = True


def stop():
    global running
    running = False


quit_button = Button("Quit Game", 300, 400, 200, 50, stop)

# Main loop
while running:
    EVENTS = pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for button clicks

    # Draw background
    screen.fill((0, 0, 0))

    # Draw title
    title = font.render("Creeper Adventure", True, (255, 255, 255))
    screen.blit(title, (250, 200))

    # Draw buttons
    start_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.update()

# Quit Pygame
pygame.quit()
