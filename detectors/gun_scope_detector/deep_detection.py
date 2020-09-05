import cv2
import numpy as np

from detectors.utils import translate, mask_diff


def find_dxy_mode(dx_dy_s, base=100):
    dxy = [dx * base + dy for dx, dy in dx_dy_s]
    counts = np.bincount(dxy)
    print(max(counts))
    dxy_mode = np.argmax(counts)
    dx = dxy_mode // base
    dy = dxy_mode % base
    return dx, dy


def sift_kp(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    # gray_image = cv2.Canny(gray_image, 50, 100)
    # cv2.imshow('gray_image', gray_image)
    # cv2.waitKey()

    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(gray_image, None)
    kp_image = cv2.drawKeypoints(gray_image, kp, None)
    return kp_image, kp, des


def sift_match(img1_3c, img2_4c):
    img2_3c = img2_4c[:, :, :3]
    kpimg1, kp1, des1 = sift_kp(img1_3c)
    kpimg2, kp2, des2 = sift_kp(img2_3c)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good_match_dx_dy_s = []
    for m, n in matches:
        x1, y1 = int(kp1[m.queryIdx].pt[0]), int(kp1[m.queryIdx].pt[1])
        x2, y2 = int(kp2[m.trainIdx].pt[0]), int(kp2[m.trainIdx].pt[1])
        good_match_dx_dy_s.append([m.distance / n.distance, n, abs(x1 - x2), abs(y1 - y2)])
    good_match_dx_dy_s = sorted(good_match_dx_dy_s)
    good_match_dx_dy_s = np.array(good_match_dx_dy_s)

    top_n = 5
    dx_dy_s = good_match_dx_dy_s[:top_n, 2:]

    dx, dy = find_dxy_mode(dx_dy_s)
    translated_img1 = translate(img1_3c, -dx, -dy)
    mask_diff_img, diff_sum = mask_diff(img2_4c[:, :, 3], img2_4c[:, :, :3], translated_img1)

    # cv2.imshow("diff", mask_diff_img)
    # match_s = good_match_dx_dy_s[:top_n, 1]
    # match_img = cv2.drawMatches(img1_3c, kp1, img2_3c, kp2, match_s, None, flags=2)
    # cv2.imshow('match_img', match_img)
    # cv2.waitKey()

    return diff_sum


if __name__ == '__main__':
    import os

    reference_dir = 'calibrate_images'
    test_dir = 'test_images'
    for test_name in os.listdir(test_dir):
        test_im = cv2.imread(os.path.join(test_dir, test_name))
        for reference_name in os.listdir(reference_dir):
            reference_im = cv2.imread(os.path.join(reference_dir, reference_name), cv2.IMREAD_UNCHANGED)

            min_h = min(reference_im.shape[0], test_im.shape[0])
            min_w = min(reference_im.shape[1], test_im.shape[1])
            reference_im = reference_im[:min_h, :min_w, :]
            test_im = test_im[:min_h, :min_w, :]

            sift_match(test_im, reference_im)
