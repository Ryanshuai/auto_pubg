import numpy as np
import cv2
from skimage.measure import label, regionprops


def get_white_shield(im, min_rgb):
    shield_rgb = np.where(im > min_rgb, 255, 0).astype(np.uint8)
    shield = shield_rgb[:, :, 0] & shield_rgb[:, :, 1] & shield_rgb[:, :, 2]
    return shield


def get_big_icon_4c(im):
    # get max_white_area---------------------------------------
    shield = get_white_shield(im, 190)

    label_im = label(shield, connectivity=shield.ndim)
    props = regionprops(label_im)

    max_area = 0
    bbox = [0, 0, 0, 0]
    for prop in props:
        area = prop.area
        if area > max_area:
            max_area = area
            bbox = prop.bbox
    y1, x1, y2, x2 = bbox
    white_area = im[y1:y2, x1:x2]
    cv2.imshow('white_area', white_area)
    cv2.waitKey()

    # get big_icon--------------------------------------------
    shield = get_white_shield(white_area, 190)
    label_im = label(255 - shield, connectivity=shield.ndim)
    props = regionprops(label_im)

    max_area = 0
    bbox = [0, 0, 0, 0]
    for prop in props:
        area = prop.area
        if area > max_area:
            max_area = area
            bbox = prop.bbox
    y1, x1, y2, x2 = bbox
    big_icon = white_area[y1:y2, x1:x2]

    # get big_icon_4c------------------------------------------
    shield = get_white_shield(big_icon, 130)
    shield = (255 - shield)[:, :, np.newaxis]
    big_icon *= (shield / 255).astype(np.uint8)
    big_icon_4c = np.concatenate((big_icon, shield), axis=-1)

    return big_icon_4c


if __name__ == '__main__':
    import os

    screen_icon_dir = 'screen_icon_template'
    icon_save_dir = 'big_icon'
    for screen_name in os.listdir(screen_icon_dir):
        screen = cv2.imread(os.path.join(screen_icon_dir, screen_name))
        big_icon_4c = get_big_icon_4c(screen)
        cv2.imwrite(icon_save_dir + '/' + screen_name, big_icon_4c)
