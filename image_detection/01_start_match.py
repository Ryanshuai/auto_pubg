import os
import cv2
import numpy as np
from pykeyboard import PyKeyboardEvent

from screen_capture import win32_cap
from image_detection.search_rects import get_image_corner
from screen_parameter import min_icon_area


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


def save_icon(im1, im2):
    rects = get_image_corner(im1)
    for rect in rects:
        x1, y1, x2, y2 = rect
        x1, y1 = x1 + 3, y1 + 3
        x2, y2 = x2 - 3, y2 - 3
        icon1 = im1[y1:y2, x1:x2]
        icon2 = im2[y1:y2, x1:x2]
        icon_diff = abs(icon1 - icon2)
        icon_diff_byte = np.where(icon_diff < 10, 0, 1).astype(np.uint8)
        icon_diff_byte = icon_diff_byte[:, :, 0] & icon_diff_byte[:, :, 1] & icon_diff_byte[:, :, 2]
        if np.sum(icon_diff_byte) > min_icon_area:
            icon_same_byte = (1 - icon_diff_byte)[:, :, np.newaxis]
            icon = icon1 * icon_same_byte
            icon = np.concatenate((icon, icon_same_byte * 255), axis=-1)
            cv2.imwrite('icons/' + str(x1) + '_' + str(y1) + '_' + str(x2) + '_' + str(y2) + '.png', icon)


if __name__ == '__main__':
    im1 = cv2.imread('0.png')
    im2 = cv2.imread('1.png')

    save_icon(im1, im2)