import numpy as np
from skimage.measure import label, regionprops

from screen_parameter import white_min_rgb
from screen_parameter import min_mk47_high, max_mk47_high, min_mk47_width, max_mk47_width
from screen_parameter import min_fire_mode_high, max_fire_mode_high, min_fire_mode_width, max_fire_mode_width
from screen_parameter import min_in_tab_high, max_in_tab_high, min_in_tab_width, max_in_tab_width


def get_white_shield(im, min_rgb=white_min_rgb):
    shield_rgb = np.where(im > min_rgb, 255, 0).astype(np.uint8)
    shield = shield_rgb[:, :, 0] & shield_rgb[:, :, 1] & shield_rgb[:, :, 2]
    return shield


def search_white_size(image, min_h, max_h, min_w, max_w):
    shield = get_white_shield(image)

    kernel = np.ones((14, 14), np.uint8)
    shield = cv2.morphologyEx(shield, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('shield', shield)
    cv2.waitKey()

    label_im = label(shield, connectivity=shield.ndim)
    props = regionprops(label_im)

    bbox_list = list()
    for prop in props:
        bbox = prop.bbox
        if min_h < (bbox[2] - bbox[0]) < max_h and min_w < (bbox[3] - bbox[1]) < max_w:
            bbox_list.append(bbox)
    return bbox_list


if __name__ == '__main__':
    import cv2

    im = cv2.imread('screens_weapon/0.png')
    bboxes = search_white_size(im, min_in_tab_high, max_in_tab_high, min_in_tab_width, max_in_tab_width)
    print('in_tab')
    shield = np.zeros_like(im, dtype=np.uint8)
    for rect in bboxes:
        y1, x1, y2, x2 = rect
        shield[y1:y2, x1:x2] = 1.0
        print([y1, x1, y2, x2])
    cv2.imshow('shield', im * shield)
    cv2.waitKey()

    im = cv2.imread('screens_fire_mode/0.png')
    bboxes = search_white_size(im, min_fire_mode_high, max_fire_mode_high, min_fire_mode_width, max_fire_mode_width)
    print('fire_mode')
    shield = np.zeros_like(im, dtype=np.uint8)
    for rect in bboxes:
        y1, x1, y2, x2 = rect
        shield[y1:y2, x1:x2] = 1.0
        print([y1, x1, y2, x2])
    cv2.imshow('shield', im * shield)
    cv2.waitKey()

    im = cv2.imread('screens_weapon/0.png')
    bboxes = search_white_size(im, min_mk47_high, max_mk47_high, min_mk47_width, max_mk47_width)
    shield = np.zeros_like(im, dtype=np.uint8)
    print('weapon?name')
    for rect in bboxes:
        y1, x1, y2, x2 = rect
        shield[y1:y2, x1:x2] = 1.0
        print([y1, x1, y2, x2])
    cv2.imshow('shield', im * shield)
    cv2.waitKey()
