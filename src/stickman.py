import pymunk
from pymunk import Vec2d
import src.shape_funcs as sf

def sum_tp(t1, t2):
    return tuple(map(sum, zip(t1, t2)))

def add_joint(space: pymunk.Space, shape1: pymunk.Segment, shape2: pymunk.Segment):
    shape2.body.position = shape1.body.position + shape1.b
    joint = sf.create_pivot_joint(space, shape1.body, shape2.body, shape2.body.position)
    return joint

class Stickman:
    
    def __init__(self, space: pymunk.Space, pos):
        seg_radius = 8
        
        self.upper_body = sf.create_segment(space, pos, Vec2d(0, 55), seg_radius)
        self.head = pymunk.Circle(self.upper_body.body, 25, (0, -25))
        space.add(self.head)

        self.lower_body = sf.create_segment(space, (0, 0), Vec2d(0, 40), seg_radius)
        joint1 = add_joint(space, self.upper_body, self.lower_body) 
        
        self.leg_left_top = sf.create_segment(space, (0, 0), Vec2d(0, 40).rotated_degrees(30), seg_radius)
        joint2 = add_joint(space, self.lower_body, self.leg_left_top)
        
        self.leg_right_top = sf.create_segment(space, (0, 0), Vec2d(0, 40).rotated_degrees(-30), seg_radius) 
        joint3 = add_joint(space, self.lower_body, self.leg_right_top)

        self.leg_left_top.filter = pymunk.ShapeFilter(group=1)
        self.leg_right_top.filter = pymunk.ShapeFilter(group=1)

        self.leg_left_bottom = sf.create_segment(space, (0, 0), Vec2d(0, 60).rotated_degrees(0), seg_radius)
        joint4 = add_joint(space, self.leg_left_top, self.leg_left_bottom)
         
        self.leg_right_bottom = sf.create_segment(space, (0, 0), Vec2d(0, 60).rotated_degrees(0), seg_radius)
        joint4 = add_joint(space, self.leg_right_top, self.leg_right_bottom)

        self.segments = [self.upper_body, self.lower_body, self.leg_left_top, self.leg_right_top, self.leg_left_bottom, self.leg_right_bottom]
        self.joints = [joint1, joint2, joint3]
