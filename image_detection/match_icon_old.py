import os
import cv2
import numpy as np
from pykeyboard import PyKeyboardEvent

from screen_capture import win32_cap
from screen_parameter import min_icon_area
from image_detection.position_constant import screen_icon_position


class Key_listener(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)
        self.is_first = True

    def tap(self, keycode, character, press):
        if keycode == 162 and press:
            if self.is_first:
                self.im1 = win32_cap()
                self.is_first = False
            else:
                self.im2 = win32_cap()
                self.is_first = True

                save_icon(self.im1, self.im2)

    def escape(self, event):
        return False


def save_icon(im0, im):
    for pos_name, rect in screen_icon_position.items():
        y1, x1, y2, x2 = rect
        icon0 = im0[y1:y2, x1:x2]
        icon = im[y1:y2, x1:x2]
        icon_diff = abs(icon - icon0)
        icon_diff_byte = np.where(icon_diff == 0, 0, 1).astype(np.uint8)
        icon_diff_byte = icon_diff_byte[:, :, 0] & icon_diff_byte[:, :, 1] & icon_diff_byte[:, :, 2]
        if np.sum(icon_diff_byte) > min_icon_area:
            icon_same_byte = (1 - icon_diff_byte)[:, :, np.newaxis]
            icon_3c = icon * icon_same_byte
            icon_name = get_icon_name(icon_3c)
            icon_4c = np.concatenate((icon_3c, icon_same_byte * 255), axis=-1)
            cv2.imwrite('icons/' + pos_name + '-' + icon_name + '.png', icon_4c)


def get_icon_name(icon):
    rint = np.random.randint(0, 1000)
    return str(rint)


if __name__ == '__main__':
    # kl = Key_listener()
    # kl.run()

    im1 = cv2.imread('test_screens_icon_match/0.png')
    im2 = cv2.imread('test_screens_icon_match/1.png')
    save_icon(im1, im2)
