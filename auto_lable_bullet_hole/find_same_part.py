import numpy as np
from skimage.measure import label, regionprops


def get_same_part(im1, im2, min_area, max_area):
    im_diff = np.abs(im1 - im2)
    im_diff = np.mean(im_diff, axis=-1)
    im_byte = np.where(im_diff == 0, 1., 0)
    cv2.imshow('  ', im_byte)
    cv2.waitKey()
    label_img = label(im_byte, connectivity=im_byte.ndim)
    props = regionprops(label_img)

    bbox_list = list()
    for prop in props:
        area = prop.area
        if min_area < area < max_area:
            bbox = prop.bbox
            bbox_list.append(bbox)
    return bbox_list


if __name__ == '__main__':
    import cv2

    im1 = cv2.imread('0.png')
    # im2 = cv2.imread('1.png')
    #
    # im1 = cv2.resize(im1, (1000, 500))
    # im2 = cv2.resize(im2, (1000, 500))
    #
    # bbox_list = get_same_part(im1, im2, 20, 200)
    #
    # for bbox in bbox_list:
    #     img = cv2.rectangle(im1, (bbox[1], bbox[0]), (bbox[3], bbox[2]), (255, 0, 0))
    # cv2.imshow('after', im1)
    # cv2.waitKey()

    im1 = np.mean(im1, axis=-1)
    im1 = np.where(im1 == 255, 255, 0).astype(np.uint8)
    cv2.imshow('im1', im1)
    cv2.waitKey()
