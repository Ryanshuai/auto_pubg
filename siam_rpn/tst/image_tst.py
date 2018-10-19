import cv2
import os
import numpy as np
import torch
from os.path import realpath, dirname, join

from model.net import SiamRPN
from model.track import Tracker
from config.siam_rpn.default_ys2_ubuntu import ARG as ys_ARG
from config.siam_rpn.default import ARG


video_path = join(realpath(dirname(__file__)), 'ILSVRC2015_test_00043016.mp4')
cap = cv2.VideoCapture(video_path)
ret, first_im = cap.read()

center_x, center_y, w, h = 340, 485, 30, 30
target_pos, target_sz = np.array([center_x, center_y]), np.array([w, h])

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
net_file = join(realpath(dirname(__file__)), 'snapshot_epoch170_model')
model.load_state_dict(torch.load(net_file))
model.eval().cuda()
tracker = Tracker(arg, first_im, target_pos, target_sz, model)

while True:
    ret, im = cap.read()
    if not ret:
        break

    x, y, w, h = tracker.track(im)

    rect_img = cv2.rectangle(im, (int(x), int(y)), (int(x+w), int(y+h)), (0, 0, 255), thickness=3)

    cv2.imshow('video_test', rect_img)
    cv2.waitKey(0)

cap.release()