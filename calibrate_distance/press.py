import threading
import os
from screen_capture import win32_cap


class Press(threading.Thread):
    def __init__(self, time_interval, length=45, image_dir=''):
        self.image_dir = image_dir
        threading.Thread.__init__(self)
        self.dist_seq, self.time_seq = [0] * length, [x * time_interval for x in range(length)]
        self._loop = True

    def run(self):
        for idx, (time, dist) in enumerate(zip(self.time_seq, self.dist_seq)):
            threading.Timer(time, self.task_func, args=[idx + 1]).start()

    def task_func(self, idx):
        if self._loop and self.image_dir:
            win32_cap(filename=self.image_dir + str(idx) + '.png', rect=(100, 100, 400, 1600))

    def stop(self):
        self._loop = False


if __name__ == '__main__':
    pass
