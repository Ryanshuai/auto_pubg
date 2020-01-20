import numpy as np
import cv2
import os
from image_detection.utils import get_white_shield


class Detector:
    def __init__(self, position, crop_dict):
        self.png_dict = dict()

        png_dir = os.path.join('D:/github_project/auto_press_down_gun/image_detect/states_4c_im', category_name)
        assert os.path.exists(png_dir)
        for png_name in reversed(os.listdir(png_dir)):
            abs_png_name = os.path.join(png_dir, png_name)
            png = cv2.imread(abs_png_name, cv2.IMREAD_UNCHANGED)
            self.png_dict[png_name[:-4]] = png

    def match_avr_thr(self, crop_im, avr_thr=10, absent_return=''):
        for item_name, png in self.png_dict.items():
            avr = detect_3d_diff_average(crop_im, png)
            if avr < avr_thr:
                return item_name
        return absent_return

    def match_white(self, crop_im, min_rgb=230, avr_thr=10, absent_return=''):
        white_shield = get_white_shield(crop_im, min_rgb).astype(np.uint8)
        for item_name, png in self.png_dict.items():
            avr = np.sum(np.abs(white_shield - png))/white_shield.size
            if avr < avr_thr:
                return item_name
        return absent_return


def detect_3d_diff_average(detect_im_3c: np.ndarray, target_im_4c: np.ndarray):
    target_im = target_im_4c[:, :, 0:3]
    shield = (target_im_4c[:, :, [3]] // 255).astype(np.uint8)
    target_im = target_im * shield

    test_im = detect_im_3c * shield
    sum = np.sum(test_im - target_im)
    average = sum / np.sum(shield)
    return average


if __name__ == '__main__':
    from auto_position_label.crop_position import crop_screen, screen_position as sc_pos

    path = '../auto_position_label/pos1.png'
    screen = cv2.imread(path)
    scope_detect = Detector('fire_mode')
    a = scope_detect.match_white(crop_screen(screen, sc_pos['fire_mode']))
    print(a)

    path = 'D:/github_project/auto_press_down_gun/temp_test_image/444.png'
    crop_im = cv2.imread(path)
    scope_detect = Detector('scope')
    a = scope_detect.match_avr_thr(crop_im)
    print(a)

    path = 'D:/github_project/auto_press_down_gun/cc.png'
    crop_im = cv2.imread(path)
    scope_detect = Detector('in_tab')
    a = scope_detect.match_avr_thr(crop_im)
    print(a)

    scope_detect = Detector('weapon1name')
