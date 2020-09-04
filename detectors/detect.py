import numpy as np
import cv2
import os

from detectors.gun_name_detector.gun_name_deep_detection import get_ocr_name
from detectors.utils import get_white_shield
from screen_parameter import max_icon_diff


class Detector:
    def __init__(self, png_dir):  # white or icon
        self.png_dict = dict()
        for png_name in os.listdir(png_dir):
            png = cv2.imread(os.path.join(png_dir, png_name), cv2.IMREAD_UNCHANGED)
            self.png_dict[png_name[:-4]] = png


class WhiteDetector(Detector):
    def __init__(self, png_dir):
        super().__init__(png_dir)

    def detect(self, crop_im, avr_thr=max_icon_diff):
        min_rgb = 240
        white_shield = get_white_shield(crop_im, min_rgb).astype(np.uint8)

        for item_name, png in self.png_dict.items():
            avr = np.sum(np.abs(white_shield - png)) / np.sum(white_shield)
            if avr < avr_thr:
                return item_name

        item_name = self.deep_detect(white_shield)
        return item_name

    def deep_detect(self, img):
        return img


class InTabDetector(WhiteDetector):
    def __init__(self):
        png_dir = "test_images"
        super().__init__(png_dir)

    def deep_detect(self, white_shield):
        item_name = get_ocr_name(white_shield)
        cv2.imwrite('in_tab_detector/test_images/type.png', white_shield)
        return item_name


class FireModeDetector(WhiteDetector):
    def __init__(self):
        png_dir = "test_images"
        super().__init__(png_dir)

    def deep_detect(self, white_shield):
        item_name = get_ocr_name(white_shield)
        cv2.imwrite('test_images/' + item_name + '.png', white_shield)
        return item_name


class PostureDetector(WhiteDetector):
    pass


class GunNameDetector(WhiteDetector):
    def __init__(self):
        png_dir = "test_images"
        super().__init__(png_dir)

    def deep_detect(self, white_shield):
        item_name = get_ocr_name(white_shield)
        cv2.imwrite('test_images/' + item_name + '.png', white_shield)
        return item_name


class DiffDetector(Detector):
    def detect(self, crop_im, avr_thr=max_icon_diff):
        for item_name, png in self.png_dict.items():
            avr = detect_3d_diff_average(crop_im, png)
            # print('test', item_name, avr)
            if avr < avr_thr:
                # print(item_name, avr)
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
