import threading
import builtins
from numpy import array

printing_lock = threading.Lock()
def print(*args, **kwargs):
    with printing_lock:
        builtins.print(*args, **kwargs)

ZERO = array((0.,0.))
X = array((1., 0.))
Y = array((0., 1.))