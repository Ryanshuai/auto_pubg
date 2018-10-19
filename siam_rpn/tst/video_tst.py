import cv2
import os
import numpy as np
import torch
from os.path import realpath, dirname, join

from model.net import SiamRPN
from model.track import Tracker
from config.siam_rpn.default_ys2_ubuntu import ARG as ys_ARG
from config.siam_rpn.default import ARG
from data.data_utils import *


video_path = './ILSVRC2015_test_00043015.mp4'
cap = cv2.VideoCapture(video_path)
ret, first_im = cap.read()

center_x, center_y, w, h = 930, 520, 80, 170
# x, y = center_x-w//2, center_y-h//2
# rect_img = cv2.rectangle(first_im, (int(x), int(y)), (int(x + w), int(y + h)), (255, 255, 0), thickness=2)
# cv2.imshow('video_test', rect_img)
# cv2.waitKey(0)

target_center_pos, target_sz = np.array([center_x, center_y]), np.array([w, h])

# rect_img = cv2.rectangle(first_im, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), thickness=1)
# cv2.imshow('video_test', rect_img)
# cv2.waitKey(0)

if os.path.exists('/home/'):
    arg = ys_ARG()
    print('ys_arg')
else:
    arg = ARG()
    print('server_arg')

# load net
model = SiamRPN().to(arg.device)
net_file = './SiamRPNBIG.model'
model.load_state_dict(torch.load(net_file))
model.eval().cuda()
tracker = Tracker(arg, first_im, target_center_pos, target_sz, model)

while True:
    ret, im = cap.read()
    if not ret:
        break

    center_pos, size = tracker.track(im)
    x, y, w, h = cxy_wh_to_rect(center_pos, size)

    rect_img = cv2.rectangle(im, (int(x), int(y)), (int(x+w), int(y+h)), (255, 255, 0), thickness=2)
    cv2.imshow('video_test', rect_img)
    cv2.waitKey(0)

cap.release()

