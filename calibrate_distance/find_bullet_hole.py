import cv2
import numpy as np
import math


class Bullet_Hole:
    def __init__(self):
        self.last_radius = 7

        self.min_radius = 4
        self.max_radius = 25
        self.min_area = 3.14*self.min_radius*self.min_radius
        self.max_area = 3.14*self.max_radius*self.max_radius

        self.height_resolution = 30
        self.bullet_hole_max_energy = 30
        self.bullet_hole_min_confidence = 253

    def find(self, im):
        im_grey = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        im_black = np.where(im_grey < self.bullet_hole_max_energy, 255, 0).astype(np.uint8)

        radius = self.detect_radius(im, self.last_radius)
        self.height_resolution = int(3*radius)

        hole_kernel = get_hole_kernel(radius)
        hole_confidence = cv2.filter2D(im_black, -1, hole_kernel)
        hole_position = np.where(hole_confidence > self.bullet_hole_min_confidence, 255, 0).astype(np.uint8)
        # cv2.imshow('hole_position111', hole_position)
        # cv2.waitKey()

        _, labels, stats, centroids = cv2.connectedComponentsWithStats(hole_position)

        res_centers = list()
        last_y1, last_area = 0, 10000
        for stat, center in zip(stats[1:], centroids[1:]):
            x0, y0, width, height, area = stat
            if abs(last_y1-y0) < self.height_resolution:
                if area > last_area:
                    res_centers.pop()
                    res_centers.append([int(center[0]), int(center[1])])
                    last_y1 = y0+height
                    last_area = area
            else:
                res_centers.append([int(center[0]), int(center[1])])
                last_y1 = y0+height
                last_area = area

        return res_centers

    def detect_radius(self, im, default_radius=7):
        im_grey = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        im_black = np.where(im_grey < self.bullet_hole_max_energy, 255, 0).astype(np.uint8)

        hole_kernel = get_hole_kernel(radius=self.min_radius)
        hole_confidence = cv2.filter2D(im_black, -1, hole_kernel)
        hole_position = np.where(hole_confidence > self.bullet_hole_min_confidence, 255, 0).astype(np.uint8)

        _, labels, stats, centroids = cv2.connectedComponentsWithStats(hole_position)
        areas = list()
        for stat in stats:
            x0, y0, width, height, area = stat
            if self.max_radius < (x0+width//2) < im.shape[1] - self.max_radius and self.max_radius < (x0+width//2) < im.shape[0] - self.max_radius :
                if self.min_area < area < self.max_area:
                    areas.append(area)

        if len(areas) == 0:
            return default_radius

        avr_area = sum(areas)//len(areas)
        min_area = min(areas)
        res_area = (avr_area+min_area)/2
        res_radius = math.floor(math.sqrt(res_area/3.14))
        # print(res_radius)
        return res_radius


def get_hole_kernel(radius=8):
    hole_kernel = np.zeros((2*radius+1, 2*radius+1))
    area = 0
    for j in range(-2*radius, 2*radius+1):
        for i in range(-2*radius, 2*radius+1):
            if np.linalg.norm(np.array([i, j]) - np.array([radius, radius])) <= radius:
                hole_kernel[i, j] = 1
                area += 1
    hole_kernel /= area
    return hole_kernel


if __name__ == '__main__':
    import os
    bh = Bullet_Hole()

    def draw_bullet_hole(rect_screen):
        bullet_hole_centers = bh.find(rect_screen)
        for center in bullet_hole_centers:
            x, y = center
            im = cv2.circle(rect_screen, (int(x), int(y)), 40, (255, 0, 255), thickness=2)

        cv2.imshow(im_path[-6:], rect_screen)
        cv2.waitKey()

    im_path = 'D:/github_project/auto_press_down_gun/press_gun/generate_distance/groza/x1r.png'
    rect_screen = cv2.imread(im_path)
    draw_bullet_hole(rect_screen)

    im_path = 'D:/github_project/auto_press_down_gun/press_gun/generate_distance/groza/x15.png'
    rect_screen = cv2.imread(im_path)
    draw_bullet_hole(rect_screen)

    im_path = 'D:/github_project/auto_press_down_gun/press_gun/generate_distance/groza/2.png'
    rect_screen = cv2.imread(im_path)
    draw_bullet_hole(rect_screen)

    # dir_path = 'D:/github_project/auto_press_down_gun/press_gun/generate_distance/generate_distance/groza/'
    # for file in os.listdir(dir_path):
    #     if file.endswith('.png'):
    #         im_path = os.path.join(dir_path, file)
    #         rect_screen = cv2.imread(im_path)
    #         draw_bullet_hole(rect_screen)
