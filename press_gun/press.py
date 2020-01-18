import threading
import win32api
import win32con
import time


class Press(threading.Thread):
    def __init__(self, dist_seq, time_seq):
        threading.Thread.__init__(self)
        self.dist_seq, self.time_seq = dist_seq, time_seq
        self._loop = True

    def run(self):
        for i in range(len(self.dist_seq)):
            if not self._loop:
                break
            dt = self.time_seq[i]
            dd = self.dist_seq[i]
            mouse_down(dd)
            time.sleep(dt)

    def stop(self):
        self._loop = False


def mouse_down(y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, int(y))


if __name__ == '__main__':
    pass

