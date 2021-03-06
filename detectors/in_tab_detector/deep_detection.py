import cv2
import numpy as np
import pytesseract
import Levenshtein
from PIL import Image
import os


def get_ocr_name(shield):
    if shield.ndim == 2:
        _shield = 255 - shield[:, :, np.newaxis]
        shield = np.concatenate((_shield, _shield, _shield), axis=-1)

    im_tess = 255 - shield
    im_tess = np.pad(im_tess, ((15, 15), (15, 15), (0, 0)), 'constant', constant_values=255)
    im_tess = cv2.GaussianBlur(im_tess, (3, 3), 1)
    pil_im_tess = Image.fromarray(cv2.cvtColor(im_tess, cv2.COLOR_BGR2RGB))
    shield_name = pytesseract.image_to_string(pil_im_tess)
    shield_name = shield_name.replace('\n', '')
    real_name = get_similar_name(shield_name)

    print('deep_detection.py: ', shield_name, '\t-->', real_name)
    # cv2.imshow('im_tess', im_tess)
    # cv2.waitKey()

    return real_name


def get_similar_name(detect_name):
    min_dist = 100
    res_gun_name = ''
    for gun_name, name_str in name_dict.items():
        dist = Levenshtein.distance(detect_name, name_str)
        dist = dist / len(name_str)
        if dist < min_dist:
            min_dist = dist
            res_gun_name = gun_name
    return res_gun_name


name_dict = {
    'type': 'type',
}

if __name__ == '__main__':
    import os

    im_dir = 'crop'
    for im_name in os.listdir(im_dir):
        im = cv2.imread(os.path.join(im_dir, im_name))
        name = get_ocr_name(im)
    print(get_similar_name("MkI4"))
