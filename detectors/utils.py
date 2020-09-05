import numpy as np
import cv2


def translate(image, x, y):
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted


def get_white_shield(img, min_rgb=None):
    if min_rgb is None:
        rgb_equal = np.equal(img[:, :, 0], img[:, :, 1]) & np.equal(img[:, :, 0], img[:, :, 2])
        rgb_equal = rgb_equal.astype(np.uint8)[:, :, np.newaxis]
        white_img = rgb_equal * img
        min_rgb = np.max(white_img) - 5

    shield_rgb = np.where(img > min_rgb, 255, 0)
    shield = shield_rgb[:, :, 0] & shield_rgb[:, :, 1] & shield_rgb[:, :, 2]
    return shield.astype(np.uint8)


def mask_diff(mask, image1, image2):
    mask = mask.astype(np.int)
    image1 = image1.astype(np.int)
    image2 = image2.astype(np.int)
    if np.max(mask) == 255:
        mask //= 255
    diff = np.abs(image1 - image2)
    diff *= mask[:, :, np.newaxis]
    diff_sum = np.sum(diff)
    diff = np.minimum(diff, 255)
    diff = diff.astype(np.uint8)
    return diff, diff_sum


if __name__ == '__main__':
    import cv2

    img = cv2.imread("2.png")
    img_shield = get_white_shield(img)
    cv2.imshow("shield", img_shield)
    cv2.waitKey()
