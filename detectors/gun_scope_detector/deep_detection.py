import random

import cv2
import numpy as np


def sift_kp(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    gray_image = cv2.Canny(gray_image, 50, 100)
    cv2.imshow('gray_image', gray_image)
    cv2.waitKey()

    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(gray_image, None)
    kp_image = cv2.drawKeypoints(gray_image, kp, None)
    return kp_image, kp, des


def xy_cluster_density(x_y_s):
    mean_x_y = np.mean(x_y_s, axis=0, keepdims=True)
    d_mean_x_y = np.sum(np.abs(x_y_s - mean_x_y))/np.shape(x_y_s)[0]

    print(d_mean_x_y)
    return d_mean_x_y


def sift_match(img1, img2, type='mode'):
    kpimg1, kp1, des1 = sift_kp(img1)
    kpimg2, kp2, des2 = sift_kp(img2)

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
    match_s = good_match_dx_dy_s[:top_n, 1]

    all_goodmatch_img = cv2.drawMatches(img1, kp1, img2, kp2, match_s, None, flags=2)

    density = xy_cluster_density(dx_dy_s)

    cv2.imshow('all_goodmatch_img', all_goodmatch_img)
    cv2.waitKey()

    return density


def detect_y_move(img1, img2, type='mode'):
    kpimg1, kp1, des1 = sift_kp(img1)
    kpimg2, kp2, des2 = sift_kp(img2)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.knnMatch(des1, des2, k=1)

    cv2.imshow('img1', kpimg1)
    cv2.imshow('img2', kpimg2)
    cv2.waitKey()

    orb = cv2.ORB_create()
    kp0, des0 = orb.detectAndCompute(img1, None)
    kp, des = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.knnMatch(des0, des, k=1)

    while [] in matches:
        matches.remove([])
    matches = sorted(matches, key=lambda x: x[0].distance)

    dy_list = list()
    img1_ = img1.copy()
    img2_ = img2.copy()
    for match in matches[0:30]:
        x0, y0 = int(kp0[match[0].queryIdx].pt[0]), int(kp0[match[0].queryIdx].pt[1])
        x, y = int(kp[match[0].trainIdx].pt[0]), int(kp[match[0].trainIdx].pt[1])
        dy_list.append(y - y0)

        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        img0_ = cv2.circle(img1_, (x0, y0), 5, (r, g, b))
        img_ = cv2.circle(img2_, (x, y), 5, (r, g, b))
        cv2.imshow('img0_', img0_)
        cv2.imshow('img_', img_)
        cv2.waitKey()
    dy_list = list(filter(lambda x: x > 0, dy_list))
    if dy_list:
        if type == 'mode':
            counts = np.bincount(dy_list)
            mode = np.argmax(counts)
            return mode
        else:
            return sum(dy_list[:10]) / 10
    return 0


if __name__ == '__main__':
    import os

    reference_dir = 'calibrate_images'
    test_dir = 'test_images'
    for test_name in os.listdir(test_dir):
        test_im = cv2.imread(os.path.join(test_dir, test_name))
        for reference_name in os.listdir(reference_dir):
            reference_im = cv2.imread(os.path.join(reference_dir, reference_name))
            reference_im = cv2.resize(reference_im, (test_im.shape[0], test_im.shape[1]))
            sift_match(test_im, reference_im)
