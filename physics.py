import time
from numpy import *
import threading
from numpy.linalg import norm
from boilerplate import *

def normed(vec):
    return vec / norm(vec)**2


class World:
    def __init__(self, *objects, size=(500, 500), dt=0.001, slowdown=0., recording=True, recording_interval=1/30):
        self.t = 0
        self.dt = dt
        self.t0 = 0
        self.size = size
        self.dim = len(size)
        self.max_speed = 1/dt

        self.real_start_time = 0
        self.real_time = 0
        self.slowdown = slowdown
        self.running = True

        self.last_frame = 0

        self.objects: [Object] = []
        self.x_record: {Object: list} = {}
        self.v_record: {Object: list} = {}
        self.f_record: {Object: list} = {}
        self.record_length = 0
        self.recording = recording
        self.recording_interval = recording_interval
        self.time_since_last_record = 0

        for obj in objects:
            self.register(obj)

    def __enter__(self):
        self.start_time = time.time()
        return self
    def __exit__(self, *junk):
        return

    def clip_vel(self, v):
        return clip(v, -1/self.dt, 1/self.dt, out=v)
        #return np.array(max(min(v[i], self.max_v[i]), -self.max_v[i]) for i in range(self.dim))

    def register(self, obj, recorded=True):
        obj.world = self
        self.objects.append(obj)
        if recorded:
            self.x_record[obj] = []
            self.v_record[obj] = []
            self.f_record[obj] = []

    def set_speed(self, speed):
        self.speed = speed
        self.frame_time = self.dt / speed

    def update(self):
        self.real_time = time.time()
        self.t += self.dt
        for object in self.objects:
            object.compute_forces()
        for object in self.objects:
            object.update()
        self.last_frame = time.time() - self.real_time

        if self.recording:
            self.time_since_last_record += self.dt
            if self.time_since_last_record >= self.recording_interval:
                self.time_since_last_record = 0
                #t = self.t
                for obj in self.x_record.keys():
                    #print('RECORDING', obj.x)
                    self.x_record[obj].append(obj.x.copy())
                    self.v_record[obj].append(obj.v.copy())
                    self.f_record[obj].append(obj.computed_forces)
                self.record_length += 1

        if self.slowdown:
            time.sleep(self.slowdown)

    def __updater_thread(self, T):
        while self.running and self.t<T:
            self.update()
    def start_simulation_thread(self, T):
        thread = threading.Thread(target=self.__updater_thread, args=(T,), daemon=True)
        thread.start()
        return thread
    def run(self, T=10000000000, debug_interval=0.3):
        thread = self.start_simulation_thread(T)
        while self.running and self.t<T:
            time.sleep(debug_interval)
            print( ' | '.join((
                'Last frame: %.4f' % round(self.last_frame, 5),
                'World time: %.4f' % round(self.t, 5),
                'Sim time: %.4f' % round(self.real_time - self.start_time, 5)
            )))
        thread.join()
        print('Simulation finished. Recorded', self.record_length, 'frames.')

class Object:
    def __init__(self, m, x, v, debug=False):
        self.x = x
        self.v = v
        self.m = m
        self.forces = []
        self.computed_forces = []

        self.triggers = []
        self.world: World = None
        self.debug = debug

    def add_forces(self, *forces):
        self.forces.extend(forces)
    def get_forces(self):
        return tuple(f(self) for f in self.forces)
    def compute_forces(self):
        self.computed_forces = self.get_forces()

    def add_trigger(self, f, condition):
        self.triggers.append((condition, f))

    def update(self):
        used_triggers = []
        for i, trigger in enumerate(self.triggers):
            if trigger[0](self):
                trigger[1](self)
                used_triggers.append(trigger)
        for trigger in used_triggers:
            self.triggers.remove(trigger)

        for f in self.computed_forces:
            self.v += f / self.m * self.world.dt
        self.world.clip_vel(self.v)
        self.x += self.v * self.world.dt

        if self.debug:
            print(' | '.join((
                'Forces: ' + str(tuple(tuple(f.tolist()) for f in self.get_forces())),
                'x = ' + str(self.x),
                'v = ' + str(self.v)
            )))