import numpy as np
import cv2
from screen_parameter import min_rect_side_len, max_rect_side_len


def get_rect_kernel(corner_len=30, thick=1):
    c_len = corner_len

    left_up_kernel = np.zeros((2 * c_len + thick, 2 * c_len + thick))
    right_up_kernel = np.zeros((2 * c_len + thick, 2 * c_len + thick))
    left_down_kernel = np.zeros((2 * c_len + thick, 2 * c_len + thick))
    right_down_kernel = np.zeros((2 * c_len + thick, 2 * c_len + thick))
    for i in range(c_len + thick):
        div = thick * (2 * c_len + thick)

        for t in range(-thick // 2, thick // 2):
            left_up_kernel[2 * c_len - i][c_len + t] = 1 / div
            left_up_kernel[c_len + t][2 * c_len - i] = 1 / div

            right_up_kernel[2 * c_len - i][c_len + t] = 1 / div
            right_up_kernel[c_len + t][i] = 1 / div

            right_down_kernel[i][c_len + t] = 1 / div
            right_down_kernel[c_len + t][i] = 1 / div

            left_down_kernel[i][c_len + t] = 1 / div
            left_down_kernel[c_len + t][2 * c_len - i] = 1 / div

    return left_up_kernel, right_up_kernel, right_down_kernel, left_down_kernel


def find_corner_by_corner_canny(corner, canny):
    corner = cv2.filter2D(canny, -1, corner)
    gray_sort = np.sort(corner.flatten())[::-1]
    coordinate = np.where(corner > gray_sort[300])
    coordinate = coordinate[::-1]
    coordinate = list(map(list, zip(*coordinate)))
    return coordinate  # (x, y)


def get_possible_rects(lu_coord, ru_coord, rd_coord, ld_coord):
    blur_thr = 2
    possible_rectangles = list()
    for x1_0, y1_0 in lu_coord:
        for x2_0, y2_0 in rd_coord:
            if min_rect_side_len < y2_0 - y1_0 < max_rect_side_len and \
                    min_rect_side_len < y2_0 - y1_0 < max_rect_side_len and \
                    abs((x2_0 - x1_0) - (y2_0 - y1_0)) < 2 * blur_thr:
                for x2_1, y1_1 in ru_coord:
                    if abs(x2_0 - x2_1) < blur_thr:
                        for x1_1, y2_1 in ld_coord:
                            if abs(x1_0 - x1_1) < blur_thr:
                                possible_rectangles.append((y1_0, x1_0, y2_0, x2_0))
    possible_rectangles = list(set(possible_rectangles))
    return possible_rectangles


def filter_rects(rects, thr=3):
    res_rects = list()
    for i in range(len(rects)):
        i_has_similar = False
        for j in range(i + 1, len(rects)):
            is_similar = True
            for t in range(4):
                if abs(rects[i][t] - rects[j][t]) >= thr:
                    is_similar = False
            if is_similar:
                i_has_similar = True
                break

        if not i_has_similar:
            res_rects.append(rects[i])

    return res_rects


def get_image_corner(image, sort=True):
    canny = cv2.Canny(image, 30, 100) / 255
    # cv2.imshow("canny", canny)
    # cv2.waitKey()
    lu_c, ru_c, rd_c, ld_c = get_rect_kernel()
    lu_coor = find_corner_by_corner_canny(lu_c, canny)
    ru_coor = find_corner_by_corner_canny(ru_c, canny)
    rd_coor = find_corner_by_corner_canny(rd_c, canny)
    ld_coor = find_corner_by_corner_canny(ld_c, canny)
    possible_rects = get_possible_rects(lu_coor, ru_coor, rd_coor, ld_coor)
    rects = filter_rects(possible_rects)
    # cp3_img = image.copy()
    # for x, y, x1, y1 in last_rects:
    #     print(x, y, x1, y1)
    #     cv2.circle(cp3_img, (x, y), 1, (0, 0, 255), -1)
    #     cv2.circle(cp3_img, (x1, y), 1, (255, 0, 0), -1)
    #     cv2.circle(cp3_img, (x1, y1), 1, (0, 255, 0), -1)
    #     cv2.circle(cp3_img, (x, y1), 1, (0, 255, 255), -1)
    # cv2.imshow('cp3_img', cp3_img)
    # cv2.waitKey()

    if sort:
        dt = np.dtype([('y1', int), ('x1', int), ('y2', int), ('x2', int)])
        rects = np.array(rects, dtype=dt)
        rects = np.sort(rects, order='y1')
    else:
        rects = np.array(rects)

    return rects


if __name__ == '__main__':
    im = cv2.imread('screens_icon_position/0.png')

    rects = get_image_corner(im)
    name = ['weapon1scope', 'weapon1muzzle', 'weapon1grip', 'weapon1magazine', 'weapon1butt',
            'weapon2scope', 'weapon2muzzle', 'weapon2grip', 'weapon2magazine', 'weapon2butt']

    rects = [[rect[0] + 3, rect[1] + 3, rect[2] - 3, rect[3] - 3] for rect in rects]
    attach_dict = dict(zip(name, rects))
    print(attach_dict)

    shield = np.zeros_like(im, dtype=np.uint8)
    for name, rect in attach_dict.items():
        y1, x1, y2, x2 = rect
        shield[y1:y2, x1:x2] = 1.0
        print(name)
        cv2.imshow('', im[y1:y2, x1:x2])
        cv2.waitKey()
    cv2.imshow('shield', im * shield)
    cv2.waitKey()
