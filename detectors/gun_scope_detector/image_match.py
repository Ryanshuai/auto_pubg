import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img1 = cv.imread("calibrate_images/x6.png")
img2 = cv.imread("test_images/666.png")

# 初始化 AKAZE 探测器
akaze = cv.AKAZE_create()
# 使用 SIFT 查找关键点和描述
kp1, des1 = akaze.detectAndCompute(img1, None)
kp2, des2 = akaze.detectAndCompute(img2, None)

# BFMatcher 默认参数
bf = cv.BFMatczher()
matches = bf.knnMatch(des1, des2, k=2)

# 旋转测试
good_matches = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good_matches.append([m])

# 画匹配点
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good_matches,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv.imwrite('matches.jpg', img3)

