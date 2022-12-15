from math import *
from physics import *
from boilerplate import *
import pygame
from pygame.locals import *


SIZE = (700, 700)
FPS = 30
def pos(x, y):
    return x + SIZE[0] // 2, -y + SIZE[1] // 2


# SET UP SIMULATION
ZERO = array((0.,0.))
X = array((1., 0.))
Y = array((0., 1.))

m = 3
g = -9.81

# ramp
l = 100
h = 10
r = sqrt(l**2 + h**2)
alpha = atan(h/l)
mu = 5
ramp_vector = array((cos(alpha), sin(alpha)))
sina = sin(alpha)
cosa = cos(alpha)

# spring
k = 5
dxmin = -sqrt(-2*m*l*g/k * (tan(alpha) + mu))
dxextra = -20
vextra = sqrt(k/m * ((dxextra+dxmin)**2 - dxmin**2))
R = vextra * cosa * (-vextra * sina - sqrt(vextra**2 * sina **2 - 2 * g * l * sina / cosa)) / g

print(R)

#block
#v_magnitude = sqrt(k / m * dxmin**2)
v = ZERO.copy() #v_magnitude * ramp_vector
x = array((-100. + dxmin + dxextra,0.))

def spring(obj):
    if obj.x[0] < -100:
        return - k * (x + 100) * X
    return ZERO

def fix_velocity_at_ramp(obj):
    obj.v = norm(obj.v) * ramp_vector
    #print('TRIGGER')
def at_ramp(obj):
    #print(obj.x[0])
    return obj.x[0] >= -1

def ramp_friction(obj):
    if l > obj.x[0] and obj.x[0] > 0:
        if norm(obj.v) > 0:
            return ramp_vector * sign(obj.v) * m * g * mu * cosa
    return ZERO
def ramp_gravity(obj):
    if l > obj.x[0] and obj.x[0] > 0:
        return ramp_vector * m * g * sina
    return ZERO

def gravity(obj):
    if obj.x[0] > l:
        return m * g * Y
    return ZERO


block = Object(m, x, v, debug=False)
block.add_forces(spring)
block.add_forces(ramp_friction)
block.add_forces(ramp_gravity)
block.add_forces(gravity)

block.add_trigger(fix_velocity_at_ramp, at_ramp)


# SIMULATE
with World(block, size=SIZE, slowdown=0, recording=True, recording_interval=1/FPS) as world:
    world.run(8)

print('Recorded', world.record_length, 'frames')
print(world.x_record[block][:10])


# DISPLAY RESULTS
pygame.init()
window = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

pygame.font.init()
FONT = pygame.font.SysFont('Calibri', 16)

running = True
frame=0
while running:
    frame += 1
    if frame == world.record_length:
        frame = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    window.fill((255,255,255))

    pygame.draw.line(window, (255,0,0), pos(-100+dxmin, -350), pos(-100+dxmin, 350))
    pygame.draw.line(window, (255, 0, 0), pos(-100, -350), pos(-100, 350))
    pygame.draw.line(window, (255, 0, 0), pos(l + R, -350), pos(l + R, 350))

    # ramp
    pygame.draw.polygon(window, (0, 0, 0), [pos(0, 0), pos(l, 0), pos(l, h)], 3)
    # floor
    pygame.draw.line(window, (0, 0, 0), pos(-350, 0), pos(350, 0), 3)

    #for obj in world.objects:
    #print(pos(*world.x_record[block][frame]))
    pygame.draw.circle(window, (0,255,0), pos(*world.x_record[block][frame]), 10)

    time_marker = FONT.render('t = %.3f' % (frame / FPS), False, (0, 0, 255))
    window.blit(time_marker, (10, 10))

    pygame.display.update()
    pygame.display.flip()
    clock.tick(FPS)




"""
1c

m = 2.
g = -9.81
C = 3.
x0 = array((2., 0.))
v0 = array((3., 0.))

test = Object(m, x0, v0, debug=True)
test.add_force(lambda obj: -norm(obj.v)*obj.v*C)
"""

"""
1a

m = 2
g = -9.81
C = 3
x0 = 0
v0 = 0

test = Object(m, x0, v0)
test.add_force(lambda obj: obj.m*g)
test.add_force(lambda obj: obj.v*obj.v*C)

sqrt(-m*g/C)
"""