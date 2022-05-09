import pygame
import pymunk
from pymunk.pygame_util import DrawOptions
from src.timer import Timer
import time
import src.shape_funcs as sf
from src.stickman import Stickman

WIDTH = 1280
HEIGHT = 720

# Setup pygame/window ----------------------------------- #
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=False)

# Functions --------------------------------------------- #
def draw_circle(surface, circle: pymunk.Circle, color= (0, 0, 0)):
    pygame.draw.circle(
        surface, color, circle.body.position + circle.offset.rotated(circle.body.angle) + scroll, circle.radius, width=0)

def draw_rectangle(surface, rectangle: pymunk.Poly, color=(0, 0, 0)):
    points = []
    for v in rectangle.get_vertices():
        point = v.rotated(rectangle.body.angle) + rectangle.body.position + scroll
        points.append(point)

    pygame.draw.polygon(
        surface, color, points, width=0)

def draw_segment(surface, segment: pymunk.Segment, color=(0, 0, 0)):
    start_pos = segment.body.position + segment.a + scroll
    end_pos = segment.body.position + segment.b.rotated(segment.body.angle) + scroll

    lv = (end_pos - start_pos).normalized()
    lnv = pymunk.Vec2d(-lv.y, lv.x) * segment.radius
    points = [start_pos + lnv, end_pos + lnv, end_pos - lnv, start_pos - lnv]

    pygame.draw.polygon(surface, color, points)
    pygame.draw.circle(surface, color, start_pos, segment.radius)
    pygame.draw.circle(surface, color, end_pos, segment.radius)

def draw_joint(surface, joint: pymunk.PivotJoint, color=(0, 0, 0)):
    pygame.draw.circle(surface, color, joint.a.position + joint.anchor_a.rotated(joint.a.angle) + scroll, 4)
    
def draw_stickman(surface, stickman: Stickman):
    draw_circle(surface, stickman.head, (97, 127, 203))

    for segment in stickman.segments:
        draw_segment(surface, segment, (97, 127, 203))

    for joint in stickman.joints:
        draw_joint(surface, joint, (180, 20, 20))

# Variables --------------------------------------------- #
scroll = pymunk.Vec2d(0, 0)

space = pymunk.Space()
space.gravity = 0, 1000
# space.collision_bias = 0.000001
count = 0

circles = []

ground = sf.create_static_rectangle(space, (640, 700), 1280, 50)

stickmen = [
    Stickman(space, (500, 100))
]

draw_options = DrawOptions(screen)

# Loop --------------------------------------------------- #
main_timer = Timer()
running = True

while running:
    # Timer -------------------------------------------------- #
    dt = main_timer.tick(60)
    framerate = main_timer.get_fps()
    pygame.display.set_caption(f'Running at {framerate :.4f}.')
    
    # Events ------------------------------------------------- #
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # segments.append(sf.create_segment(
                #     space, pygame.mouse.get_pos(), (80, 0), 10))
                stickmen.append(Stickman(space, pygame.mouse.get_pos() - scroll))
                
    keys = pygame.key.get_pressed()
    
    speed = 800
    if keys[pygame.K_UP]:
        scroll += (0, speed * dt)
    if keys[pygame.K_DOWN]:
        scroll += (0, -speed * dt)
    if keys[pygame.K_LEFT]:
        scroll += (speed * dt, 0)
    if keys[pygame.K_RIGHT]:
        scroll += (-speed * dt, 0)
                
    # Update Logic -------------------------------------------- #
    space.step(dt/2)
    space.step(dt/2)
                
    # Background --------------------------------------------- #
    screen.fill((200, 200, 200))
    
    # Render ------------------------------------------------- #
    draw_rectangle(screen, ground, (165, 102, 42))
    
    for stickman in stickmen:
        draw_stickman(screen, stickman)

    # space.debug_draw(draw_options)

    # Update Display ------------------------------------------------- #
    pygame.display.flip()
