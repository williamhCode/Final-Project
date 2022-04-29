import pymunk

def create_circle(space: pymunk.Space, pos, radius, density=1):
    body = pymunk.Body()
    body.position = pos

    shape = pymunk.Circle(body, radius)
    shape.density = density
    shape.friction = 0.5
    # shape.elasticity = 0.5

    space.add(body, shape)
    return shape

def create_rectangle(space: pymunk.Space, pos, width, height, density=1):
    body = pymunk.Body()
    body.position = pos

    shape = pymunk.Poly.create_box(body, (width, height))
    shape.density = density
    shape.friction = 0.5
    # shape.elasticity = 1.0

    space.add(body, shape)
    return shape

def create_static_rectangle(space: pymunk.Space, pos, width, height):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos

    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = 0.5
    shape.elasticity = 0.5

    space.add(body, shape)
    return shape

def create_segment(space: pymunk.Space, pos, endpoint, radius, density=1):
    body = pymunk.Body()
    body.position = pos
    
    shape = pymunk.Segment(body, (0, 0), endpoint, radius)
    shape.density = density
    shape.friction = 0.5
    shape.elasticity = 0.5
    
    space.add(body, shape)
    return shape

def create_pivot_joint(space: pymunk.Space, body1, body2, *args, collide=False):
    joint = pymunk.PivotJoint(body1, body2, *args)
    joint.collide_bodies = collide
    space.add(joint)
    return joint
