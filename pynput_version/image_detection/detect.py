import numpy as np
import cv2
import os
from image_detection.utils import get_white_shield
from screen_parameter import white_min_rgb, min_white_rate, max_icon_diff


class Detector:
    def __init__(self, pos_name, type='white', default=''):  # white or icon
        self.type = type
        self.default = default
        self.png_dict = dict()
        self.pos_name = pos_name
        png_dir = os.path.join('calibrate_icons/position_icon', pos_name)
        assert os.path.exists(png_dir)
        for png_name in os.listdir(png_dir):
            png = cv2.imread(os.path.join(png_dir, png_name), cv2.IMREAD_UNCHANGED)
            self.png_dict[png_name[:-4]] = png

    def detect(self, crop_im):
        if self.type == 'white':
            name = self.match_white(crop_im)
        else:
            name = self.match_avr_thr(crop_im)
        return name

    def match_avr_thr(self, crop_im, avr_thr=max_icon_diff):
        for item_name, png in self.png_dict.items():
            avr = detect_3d_diff_average(crop_im, png)
            # print('test', item_name, avr)
            if avr < avr_thr:
                # print(item_name, avr)
                return item_name
        return self.default

    def match_white(self, crop_im, avr_thr=min_white_rate):
        min_rgb = white_min_rgb.get(self.pos_name, 240)
        white_shield = get_white_shield(crop_im, min_rgb).astype(np.uint8)
        if self.pos_name == 'posture':
            cv2.imshow('white_shield', white_shield)
            cv2.waitKey()
        if np.sum(white_shield) == 0:
            return self.default
        for item_name, png in self.png_dict.items():
            avr = np.sum(np.abs(white_shield - png)) / np.sum(white_shield)
            # cv2.imwrite('detection_debug_image/' + item_name + str(avr) + '.png', png)
            # cv2.imwrite('detection_debug_image/target.png', white_shield)
            print('test', item_name, avr)
            if avr < avr_thr:
                print(item_name, avr)
                return item_name
        return self.default


def detect_3d_diff_average(detect_im_3c: np.ndarray, target_im_4c: np.ndarray):
    target_im = target_im_4c[:, :, 0:3]
    shield = (target_im_4c[:, :, [3]] // 255).astype(np.uint8)
    target_im = target_im * shield

    test_im = detect_im_3c * shield
    sum = np.sum(test_im - target_im)
    average = sum / np.sum(shield)
    return average


if __name__ == '__main__':
    pass
