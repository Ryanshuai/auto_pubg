import cv2

from detectors.detect import WhiteDetector
from detectors.in_tab_detector.deep_detection import get_ocr_name


class InTabDetector(WhiteDetector):
    def __init__(self):
        png_dir = "test_images"
        super().__init__(png_dir)

    def deep_detect(self, white_shield):
        item_name = get_ocr_name(white_shield)
        cv2.imwrite('test_images/' + item_name + '.png', white_shield)
        return item_name


if __name__ == '__main__':
    pass
