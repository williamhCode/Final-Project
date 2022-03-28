import pygame
from timer import Timer

WIDTH = 1280
HEIGHT = 720

# Setup pygame/window ----------------------------------- #
# pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Loop --------------------------------------------------- #
main_timer = Timer()
running = True

while running:
    # Events ------------------------------------------------- #
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
    # Timer -------------------------------------------------- #
    dt = main_timer.tick(60)
    framerate = main_timer.get_fps()
    pygame.display.set_caption(f'Running at {framerate :.4f}.')
                
    # Background --------------------------------------------- #
    screen.fill((100, 0, 0))
    
    # Update ------------------------------------------------- #
    pygame.display.flip()
            
            