import threading
import win32api
import win32con
import time
from pynput.mouse import Controller


class Press(threading.Thread):
    def __init__(self, dx_s, dy_s, t_s):
        threading.Thread.__init__(self)
        self.dx_s = dx_s
        self.dy_s = dy_s
        self.t_s = t_s
        self._loop = True
        self.mouse_controller = Controller()

    def run(self):
        for dx, dy, t in zip(self.dx_s, self.dy_s, self.t_s):
            threading.Timer(t, self.mouse_move, args=[t, dx, dy]).start()

    def mouse_move(self, t, dx, dy):
        if self._loop:
            self.mouse_controller.move(dx=dx, dy=dy)

    def stop(self):
        self._loop = False


if __name__ == '__main__':
    import numpy as np

    t_s = np.arange(0, 1, 0.01)
    l = len(t_s)
    pr = Press([1000 / l] * l, [1000 / l] * l, t_s)

    pr.run()
