import cv2
import os

from press_gun.generate_distance.find_bullet_hole import Bullet_Hole
from all_states import can_full_guns


# can_full_guns = ['m762']

bh = Bullet_Hole()

gun_dist_dict = dict()
for gun_name in can_full_guns:
    one_gun_dist_list = list()
    for i in range(len(os.listdir(gun_name))+100):
        im_path = os.path.join(gun_name, str(i) + '.png')
        if not os.path.exists(im_path):
            continue
        im = cv2.imread(im_path)

        hole_centers = bh.find(im)
        if len(hole_centers) <= 1:
            break
        x0, y0 = hole_centers[-1]
        x1, y1 = hole_centers[-2]

        # im = cv2.circle(im, (x0, y0), 5, (255, 0, 255), thickness=20)
        # im = cv2.circle(im, (x1, y1), 5, (255, 255, 0), thickness=20)
        # cv2.imshow(gun_name, im)
        # cv2.waitKey(500)

        one_gun_dist_list.append(int((y0 - y1) / 12))

    # 合并第一二个
    a,b = one_gun_dist_list[0], one_gun_dist_list[1:]
    b[0] += a
    one_gun_dist_list = b

    # 加冗余
    for _ in range(10):
        one_gun_dist_list.append(one_gun_dist_list[-1])


    print("'"+gun_name+"': " + str(one_gun_dist_list) + ',')
    gun_dist_dict[gun_name] = one_gun_dist_list

print(gun_dist_dict)