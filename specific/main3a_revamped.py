from math import *
from physics import *
from boilerplate import *
import graphics

# SET UP SIMULATION
ZERO = array((0.,0.))
X = array((1., 0.))
Y = array((0., 1.))

m = 3
g = -9.81

# ramp
l = 200
h = 200
r = sqrt(l**2 + h**2)
alpha = atan(h/l)
mu = 5
ramp_vector = array((cos(alpha), sin(alpha)))
sina = sin(alpha)
cosa = cos(alpha)

# spring
k = 5
dxmin = -sqrt(-2*m*l*g/k * (tan(alpha) + mu))
dxextra = 0#-20
vextra = sqrt(k/m * ((dxextra+dxmin)**2 - dxmin**2))
R = 10000#vextra * cosa * (-vextra * sina - sqrt(vextra**2 * sina **2 - 2 * g * l * sina / cosa)) / g

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
block.add_forces(spring, ramp_friction, ramp_gravity, gravity)
block.add_trigger(fix_velocity_at_ramp, at_ramp)


# SIMULATE
SIZE = (700, 700)
FPS = 30
with World(block, size=SIZE, recording_interval=1/FPS) as world:
    world.run(8)

# DISPLAY RESULTS
app = graphics.Window(SIZE)

app.vert_line(-100 + dxmin)
app.vert_line(-100)
app.vert_line(l + R)

app.polygon((0, 0), (l, 0), (l, h))
app.horiz_line(0, line_width=3, color=graphics.BLACK)
app.dynamic_circle(lambda: world.x_record[block][app.frame_counter], lambda: 10)

app.dynamic_label(lambda: 't = %.3f' % (app.frame_counter / FPS))
app.dynamic_label(lambda: 'f = %d' % (app.frame_counter))
app.dynamic_label(lambda: 'v = %.3f' % (norm(world.v_record[block][app.frame_counter])))

app.set_loop(world.record_length)

while app.running:
    app.draw()
