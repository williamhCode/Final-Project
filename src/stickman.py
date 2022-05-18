from pymunk import Vec2d, Space, Circle, Segment, ShapeFilter, Arbiter
import src.shape_funcs as sf
import math, time, random
import numpy as np
import tensorflow as tf
tf.config.set_visible_devices([], 'GPU')
from tensorflow.keras.initializers import RandomNormal

from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer


def sum_tp(t1, t2):
    return tuple(map(sum, zip(t1, t2)))


def add_joint_and_motor(space: Space, shape1: Segment, shape2: Segment, angle_offset, rotation_limit):
    angle_offset = math.radians(angle_offset)
    rotation_limit = math.radians(rotation_limit)

    shape2.body.angle = shape2.body.angle + angle_offset
    shape2.body.position = shape1.body.position + shape1.b.rotated(shape1.body.angle)
    joint = sf.create_pivot_joint( space, shape1.body, shape2.body, shape2.body.position)
    sf.create_rotary_limit_joint( space, shape1.body, shape2.body, -rotation_limit, rotation_limit)

    motor = None
    motor = sf.create_simple_motor(space, shape1.body, shape2.body, 0)
    motor.max_force = 100000000

    return joint, motor


class Stickman:

    def __init__(self, space: Space, pos, id: int):
        seg_radius = 6

        self.upper_body = sf.create_segment(space, pos, Vec2d(0, 30), seg_radius)
        self.head = Circle(self.upper_body.body, 20, (0, -20))
        space.add(self.head)

        self.lower_body = sf.create_segment(space, (0, 0), Vec2d(0, 25), seg_radius)
        joint1, self.motor1 = add_joint_and_motor( space, self.upper_body, self.lower_body, 0, 20)

        self.leg_left_top = sf.create_segment(space, (0, 0), Vec2d(0, 30), seg_radius)
        joint2, self.motor2 = add_joint_and_motor( space, self.lower_body, self.leg_left_top, 30, 80)

        self.leg_right_top = sf.create_segment(space, (0, 0), Vec2d(0, 30), seg_radius)
        joint3, self.motor3 = add_joint_and_motor( space, self.lower_body, self.leg_right_top, -30, 80)

        self.leg_left_bottom = sf.create_segment(space, (0, 0), Vec2d(0, 40), seg_radius)
        joint4, self.motor4 = add_joint_and_motor(space, self.leg_left_top, self.leg_left_bottom, 10, 80)

        self.leg_right_bottom = sf.create_segment(space, (0, 0), Vec2d(0, 40), seg_radius)
        joint5, self.motor5 = add_joint_and_motor(space, self.leg_right_top, self.leg_right_bottom, -10, 80)

        self.segments = [self.upper_body, self.lower_body, self.leg_left_top, self.leg_right_top, self.leg_left_bottom, self.leg_right_bottom]
        self.joints = [joint1, joint2, joint3, joint4, joint5]
        self.motors = [self.motor1, self.motor2, self.motor3, self.motor4, self.motor5]

        for shape in self.segments:
            shape.filter = ShapeFilter(group=1)
        self.head.filter = ShapeFilter(group=1)

        # create neural network for the stickman
        self.brain = Sequential()
        self.brain.add(InputLayer(input_shape=(12,)))
        # self.brain.add(Dense(10, input_shape=(12,), activation='relu', kernel_initializer='random_normal', bias_initializer='random_normal'))
        self.brain.add(Dense(10, activation='tanh', kernel_initializer=RandomNormal(mean=0, stddev = 1), bias_initializer='random_normal'))
        self.brain.add(Dense(5, activation='tanh', kernel_initializer=RandomNormal(mean=0, stddev = 1), bias_initializer='random_normal'))

        collision_type = id + 2
        self.head.collision_type = collision_type
        self.upper_body.collision_type = collision_type
        self.lower_body.collision_type = collision_type
        self.leg_left_top.collision_type = collision_type
        self.leg_right_top.collision_type = collision_type
        
        collision_handler = space.add_collision_handler(collision_type, 1)
        collision_handler.begin = self.died

        self.dead = False
        self.death_time = None
        
        self.color = random.choices(range(256), k=3)
        
    JOINTS_SPEED = 3
    def update_speeds(self):
        inputs = [shape.body.angle for shape in self.segments] \
        + [shape.body.angular_velocity for shape in self.segments]
        # print(inputs)
        
        # t1 = time.perf_counter()
        outputs = self.brain(np.array([inputs]))[0]
        # t2 = time.perf_counter()
        # print(t2 - t1)
        # print(outputs)
        
        for i, motor in enumerate(self.motors):
            motor.rate = outputs[i] * self.JOINTS_SPEED
        
        if self.upper_body.body.position.y > 1000:
            self.dead = True
            for motor in self.motors:
                motor.rate = 0
                motor.max_force = 0

    def died(self, arbiter: Arbiter, space, data):
        if self.dead:
            return True
        
        self.dead = True
        for motor in self.motors:
            motor.rate = 0
            motor.max_force = 0
        # print(f'{arbiter.shapes[0].collision_type - 2} died')
        return True