from math import *
from physics import *
from boilerplate import *
import graphics
from numpy import *
import numpy.random
import random
import numpy as np

G = 1000000

def gravity(obj):
    forces = (clip(G * obj.m * o.m / dot(r:=obj.x-o.x, r), 0, 100) * normed(o.x-obj.x) for o in obj.world.objects if o is not obj)
    return sum(forces)


im1 = np.array([1, -1])
im2= np.array([1, -1])
im3 = np.array([1, -1])
im4 = np.array([1, -1])


particles = []
for _ in range(3):
    p = Object(random.random()*2, numpy.random.rand(3) * 100, numpy.random.rand(3) * 30)
    particles.append(p)
    p.add_forces(gravity)

V = add.reduce([l.v for l in particles]) / len(particles)
for p in particles:
    p.v -= V
X = add.reduce([l.x for l in particles]) / len(particles)
for p in particles:
    p.x -= X

# SIMULATE
SIZE = (700, 700)
FPS = 30
with World(*particles, size=SIZE, recording_interval=1/FPS) as world:
    world.run(20)

# DISPLAY RESULTS
app = graphics.Window(SIZE)

app.dynamic_circle(lambda: world.x_record[particles[0]][app.frame_counter], lambda: particles[0].m*10+5, color=graphics.BLUE)
app.dynamic_circle(lambda: world.x_record[particles[1]][app.frame_counter], lambda: particles[1].m*10+5, color=graphics.BLUE)
app.dynamic_circle(lambda: world.x_record[particles[2]][app.frame_counter], lambda: particles[2].m*10+5, color=graphics.BLUE)


#app.dynamic_circle(lambda: world.x_record[particles[i]][app.frame_counter], lambda: p.m*10+5, color=graphics.BLUE)

app.dynamic_label(lambda: 't = %.3f' % (app.frame_counter / FPS))
#for i, p in enumerate(particles):
#app.dynamic_label(lambda: 'f = %d' % (app.frame_counter))
#app.dynamic_label(lambda: 'v = %.3f' % (norm(world.v_record[block][app.frame_counter])))

app.set_loop(world.record_length)

while app.running:
    app.draw()
