import cv2
import numpy as np
import os


def detect_y_move(img0, img, type='mode'):
    orb = cv2.ORB_create()
    kp0, des0 = orb.detectAndCompute(img0, None)
    kp, des = orb.detectAndCompute(img, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.knnMatch(des0, des, k=1)

    while [] in matches:
        matches.remove([])
    matches = sorted(matches, key=lambda x: x[0].distance)

    dy_list = list()
    for match in matches[0:30]:
        x0, y0 = int(kp0[match[0].queryIdx].pt[0]), int(kp0[match[0].queryIdx].pt[1])
        x, y = int(kp[match[0].trainIdx].pt[0]), int(kp[match[0].trainIdx].pt[1])
        dy_list.append(y - y0)

        img0 = cv2.circle(img0, (x0, y0), 5, (255, 255, 0))
        img = cv2.circle(img, (x, y), 5, (255, 255, 0))
        cv2.imshow('img0', img0)
        cv2.imshow('img', img)
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
    img1 = cv2.imread("0.png")
    img2 = cv2.imread("big_icon/x4.png")

    dy = detect_y_move(img1, img2)
    print(dy)

    # y_list = detect_dir('image_match_dir/m762/4/')
    # print(y_list)
