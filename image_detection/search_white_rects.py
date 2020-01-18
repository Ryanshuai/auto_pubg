import numpy as np
from skimage.measure import label, regionprops

from screen_parameter import white_min_rgb, min_mk47_high, max_mk47_high, min_mk47_width, max_mk47_width


def get_white_shield(im, min_rgb=230):
    shield_rgb = np.where(im > min_rgb, 255, 0).astype(np.uint8)
    shield = shield_rgb[:, :, 0] & shield_rgb[:, :, 1] & shield_rgb[:, :, 2]
    return shield


def search_white_size(shield, min_h=min_mk47_high, max_h=max_mk47_high, min_w=min_mk47_width, max_w=max_mk47_width):
    kernel = np.ones((14, 14), np.uint8)
    shield = cv2.morphologyEx(shield, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('shield', shield)
    cv2.waitKey()

    label_im = label(shield, connectivity=shield.ndim)
    props = regionprops(label_im)

    bbox_list = list()
    for prop in props:
        bbox = prop.bbox
        if min_h < (bbox[3] - bbox[1]) < max_h and min_w < (bbox[2] - bbox[0]) < max_w:
            bbox_list.append(bbox)
    return bbox_list


if __name__ == '__main__':
    import cv2

    im = cv2.imread('screens_icon_position/0.png')

    shield = get_white_shield(im)
    bboxes = search_white_size(shield)

    shield = np.zeros_like(im, dtype=np.uint8)
    for rect in bboxes:
        y1, x1, y2, x2 = rect
        shield[y1:y2, x1:x2] = 1.0
    cv2.imshow('shield', im * shield)
    cv2.waitKey()

