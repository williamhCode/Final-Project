from pymunk import Vec2d, Space, Circle, Segment, ShapeFilter
import src.shape_funcs as sf
import math

def sum_tp(t1, t2):
    return tuple(map(sum, zip(t1, t2)))

def add_joint_and_motor(space: Space, shape1: Segment, shape2: Segment, angle_offset, rotation_limit):
    angle_offset = math.radians(angle_offset)
    rotation_limit = math.radians(rotation_limit)
    
    shape2.body.angle = shape2.body.angle + angle_offset
    shape2.body.position = shape1.body.position + shape1.b.rotated(shape1.body.angle)
    joint = sf.create_pivot_joint(space, shape1.body, shape2.body, shape2.body.position)
    sf.create_rotary_limit_joint(space, shape1.body, shape2.body, -rotation_limit, rotation_limit)
    
    motor = None
    motor = sf.create_simple_motor(space, shape1.body, shape2.body, 0)
    motor.max_force = 100000000
    
    return joint, motor


class Stickman:
    
    def __init__(self, space: Space, pos):
        seg_radius = 8
        
        self.upper_body = sf.create_segment(space, pos, Vec2d(0, 50), seg_radius)
        self.head = Circle(self.upper_body.body, 25, (0, -25))
        space.add(self.head)

        self.lower_body = sf.create_segment(space, (0, 0), Vec2d(0, 35), seg_radius)
        joint1, self.motor1 = add_joint_and_motor(space, self.upper_body, self.lower_body, 0, 30)
        
        self.leg_left_top = sf.create_segment(space, (0, 0), Vec2d(0, 40), seg_radius)
        joint2, self.motor2 = add_joint_and_motor(space, self.lower_body, self.leg_left_top, 30, 30)
        
        self.leg_right_top = sf.create_segment(space, (0, 0), Vec2d(0, 40), seg_radius) 
        joint3, self.motor3 = add_joint_and_motor(space, self.lower_body, self.leg_right_top, -30, 30)

        self.leg_left_bottom = sf.create_segment(space, (0, 0), Vec2d(0, 60), seg_radius)
        joint4, self.motor4 = add_joint_and_motor(space, self.leg_left_top, self.leg_left_bottom, 10, 30)
         
        self.leg_right_bottom = sf.create_segment(space, (0, 0), Vec2d(0, 60), seg_radius)
        joint5, self.motor5 = add_joint_and_motor(space, self.leg_right_top, self.leg_right_bottom, -10, 30)

        self.segments = [self.upper_body, self.lower_body, self.leg_left_top, self.leg_right_top, self.leg_left_bottom, self.leg_right_bottom]
        self.joints = [joint1, joint2, joint3, joint4, joint5]

        for shape in self.segments:
            shape.filter = ShapeFilter(group=1)
        self.head.filter = ShapeFilter(group=1)
