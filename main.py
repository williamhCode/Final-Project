import pygame
import pymunk
from pymunk.pygame_util import DrawOptions
from src.timer import Timer
import random, copy
import src.shape_funcs as sf
from src.stickman import Stickman
import numpy as np
import multiprocessing


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
    draw_circle(surface, stickman.head, (stickman.color))

    for segment in stickman.segments:
        draw_segment(surface, segment, (stickman.color))

    # for joint in stickman.joints:
    #     draw_joint(surface, joint, (180, 20, 20))

def generate_stickmen():
    return [Stickman(space, (starting_xpos, 530), i) for i in range(NUM_STICKMAN)]

def mutate_weights(weights: list[np.ndarray], mutation_rate):
    # mutate each models weights
    for i in range(len(weights)):
        for index, x in np.ndenumerate(weights[i]):
            if(random.random() < mutation_rate):
                weights[i][index] = random.uniform(-1, 1)

    return weights

def reset():    
    global space, stickmen, ground, fitnesses, generation, time

    # for stickman in stickmen:
    #     if stickman.death_time is None:
    #         stickman.death_time = time
    
    for i, stickman in enumerate(stickmen):
        fitnesses[i] = (stickman.lower_body.body.position.x - starting_xpos) / 100 
        # + (stickman.death_time) / 20

    weights_list = [stickmen[i].brain.get_weights() for i in range(NUM_STICKMAN)]
    # print(weights_list[0])
    
    index_1 = np.argmax(fitnesses)
    fitnesses[index_1] = float('-inf')
    index_2 = np.argmax(fitnesses)
    
    parent1_weights = weights_list[index_1]
    parent2_weights = weights_list[index_2]
    
    crossover_index = random.randint(0, len(parent1_weights) - 1)
    parent1 = parent1_weights[:crossover_index]
    parent2 = parent2_weights[crossover_index:]
    child_weights = parent1 + parent2
    child_weights = parent1_weights
    
    new_weights_list = [mutate_weights(copy.deepcopy(child_weights), i/NUM_STICKMAN * 0.3) for i in range(NUM_STICKMAN)]

    space = pymunk.Space()
    space.gravity = 0, 1000

    # ground = sf.create_static_rectangle(space, (640, 700), 5000, 50)
    ground = sf.create_static_rectangle(space, (1600, 700), 3000, 50)
    ground.collision_type = 1
    
    generation += 1
    fitnesses = [0] * NUM_STICKMAN
    
    stickmen = generate_stickmen()
    for i in range(NUM_STICKMAN):
        stickmen[i].brain.set_weights(new_weights_list[i])
        
    time = 0

def main():
    WIDTH = 1280
    HEIGHT = 720

    # Setup pygame/window ----------------------------------- #
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=False)
    
    global NUM_STICKMAN, stickmen, starting_xpos, generation, time, fitnesses, space, ground, scroll
    
    # Variables --------------------------------------------- #
    scroll = pymunk.Vec2d(0, 0)
    NUM_STICKMAN = 20
    game_speed = 1
    generation = 0
    alive_time = 20
    follow_best = False
    starting_xpos = 500

    font = pygame.font.SysFont('Comic Sans MS', 22)

    # have to reset variables before starting --------------- #
    space = pymunk.Space()
    space.gravity = 0, 1000

    # ground = sf.create_static_rectangle(space, (640, 700), 5000, 50)
    ground = sf.create_static_rectangle(space, (1600, 700), 3000, 50)
    ground.collision_type = 1

    fitnesses = [0] * NUM_STICKMAN
    stickmen = generate_stickmen()

    # Loop --------------------------------------------------- #
    main_timer = Timer()
    running = True

    time = 0
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
                    
                if event.key == pygame.K_r:
                    reset()
                    
                if event.key == pygame.K_EQUALS:
                    game_speed += 1
                    print(f'{game_speed=}')

                if event.key == pygame.K_MINUS:
                    game_speed -= 1
                    game_speed = max(1, game_speed)
                    print(f'{game_speed=}')
                    
                if event.key == pygame.K_f:
                    follow_best = not follow_best
                    
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
        for _ in range(game_speed):
            for stickman in stickmen:
                stickman.update_speeds()  
            space.step(1/60)
            time += 1/60
            
        if (time > alive_time):
            reset()
            
        for stickman in stickmen:
            if stickman.death_time is None and stickman.dead:
                stickman.death_time = time
                
        if all(stickman.dead for stickman in stickmen):
            reset()
                    
        # Background --------------------------------------------- #
        screen.fill((200, 200, 200))
        
        # Render ------------------------------------------------- #
        draw_rectangle(screen, ground, (165, 102, 42))
        
        if follow_best:
            x_positions = [stickman.upper_body.body.position.x for stickman in stickmen]
            draw_stickman(screen, stickmen[np.argmax(x_positions)])
        else:
            for stickman in stickmen:
                draw_stickman(screen, stickman)

        # draw text
        generation_txt = font.render(f'Generation: {generation}', False, (0, 0, 0))
        screen.blit(generation_txt, (25, 20))
        
        time_txt = font.render(f'Time: {time:.1f}', False, (0, 0, 0))
        screen.blit(time_txt, (25, 50))
        
        speed_txt = font.render(f'Speed: {game_speed * 1 / dt / 60:.1f}', False, (0, 0, 0))
        screen.blit(speed_txt, (25, 80))

        # Update Display ------------------------------------------------- #
        pygame.display.flip()

if __name__ == '__main__':
    main()