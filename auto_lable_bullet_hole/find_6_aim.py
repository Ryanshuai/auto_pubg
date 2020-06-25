import cv2
import numpy as np
from skimage.measure import label, regionprops


def get_6_aim_point(im):
    assert im.ndim == 3
    b = im[:, :, 0]
    g = im[:, :, 1]
    r = im[:, :, 2]
    r = np.where(r > 230, 1, 0)
    g = np.where(g < 170, 1, 0)
    b = np.where(b < 100, 1, 0)
    a = r & g & b
    # a = (a * 255).astype(np.uint8)
    label_img = label(a, connectivity=a.ndim)
    props = regionprops(label_img)
    for prop in props:
        if prop.area < 20:
            return prop.bbox


if __name__ == '__main__':
    for i in range(36):
        im_name = str(i) + '.png'
        im = cv2.imread(im_name)
        im = cv2.resize(im, (2000, 1000))
        # im = im[500:900, 1600:1800]
        bb = get_6_aim_point(im)
        print(bb)
