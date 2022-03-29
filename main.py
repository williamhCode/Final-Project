import pygame
import pymunk
from timer import Timer

WIDTH = 1280
HEIGHT = 720

# Setup pygame/window ----------------------------------- #
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Functions --------------------------------------------- #
def draw_circle(surface, circle: pymunk.Circle):
    pygame.draw.circle(
        surface, (255, 255, 255), circle.body.position, circle.radius, width=1)

def create_circle(space: pymunk.Space, pos, mass, radius):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = pos
    
    shape = pymunk.Circle(body, radius)
    shape.friction = 0.5
    # shape.elasticity = 0.5
    
    space.add(body, shape)
    return shape

def draw_rectangle(surface, rectangle: pymunk.Poly):
    points = []
    for v in rectangle.get_vertices():
        point = v.rotated(rectangle.body.angle) + rectangle.body.position
        points.append(point)
        
    pygame.draw.polygon(
        surface, (255, 255, 255), points, width=1)

def create_rectangle(space: pymunk.Space, pos, mass, width, height):
    moment = pymunk.moment_for_box(mass, (width, height))
    body = pymunk.Body(mass, moment)
    body.position = pos
    
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    # shape.elasticity = 1.0
    
    space.add(body, shape)
    return shape

def create_static_rectangle(space: pymunk.Space, pos, width, height):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    # shape.elasticity = 0.5
    
    space.add(body, shape)
    return shape

# Variables --------------------------------------------- #
space = pymunk.Space()
space.gravity = 0, 1000

circles = []
# circles.append(create_circle(space, (100, 100), 1, 50))

rectangles = []
rectangles.append(create_static_rectangle(space, (640, 700), 1280, 50))

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
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                circles.append(create_circle(space, pygame.mouse.get_pos(), 1, 30))
                
    # Timer -------------------------------------------------- #
    dt = main_timer.tick(60)
    framerate = main_timer.get_fps()
    pygame.display.set_caption(f'Running at {framerate :.4f}.')
    
    # Update Logic -------------------------------------------- #
    space.step(dt)
                
    # Background --------------------------------------------- #
    screen.fill((100, 0, 0))
    
    # Render ------------------------------------------------- #
    for circle in circles:
        draw_circle(screen, circle)
        
    for rectangle in rectangles:
        draw_rectangle(screen, rectangle)
    
    # Update Display ------------------------------------------------- #
    pygame.display.flip()
            
            