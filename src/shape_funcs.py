from pymunk import Space, Body, Circle, Poly, Segment, PivotJoint, SimpleMotor, RotaryLimitJoint

def create_circle(space: Space, pos, radius, density=1):
    body = Body()
    body.position = pos

    shape = Circle(body, radius)
    shape.density = density
    shape.friction = 0.5
    # shape.elasticity = 0.5

    space.add(body, shape)
    return shape

def create_rectangle(space: Space, pos, width, height, density=1):
    body = Body()
    body.position = pos

    shape = Poly.create_box(body, (width, height))
    shape.density = density
    shape.friction = 0.5
    # shape.elasticity = 1.0

    space.add(body, shape)
    return shape

def create_static_rectangle(space: Space, pos, width, height):
    body = Body(body_type=Body.STATIC)
    body.position = pos

    shape = Poly.create_box(body, (width, height))
    shape.friction = 0.5
    shape.elasticity = 0.5

    space.add(body, shape)
    return shape

def create_segment(space: Space, pos, endpoint, radius, density=1):
    body = Body()
    body.position = pos
    
    shape = Segment(body, (0, 0), endpoint, radius)
    shape.density = density
    shape.friction = 0.5
    shape.elasticity = 0.5
    
    space.add(body, shape)
    return shape

def create_pivot_joint(space: Space, body1, body2, *args):
    joint = PivotJoint(body1, body2, *args)
    space.add(joint)
    return joint

def create_simple_motor(space: Space, body1, body2, rate):
    motor = SimpleMotor(body1, body2, rate)
    space.add(motor)
    return motor

def create_rotary_limit_joint(space: Space, body1, body2, min, max):
    joint = RotaryLimitJoint(body1, body2, min, max)
    space.add(joint)
    return joint