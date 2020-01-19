import os
import win32api
import win32con
import time
import cv2
from pykeyboard import PyKeyboardEvent
from PyQt5.QtCore import pyqtSignal, QObject

from all_states import All_States
from press_gun.generate_distance.find_bullet_hole import Bullet_Hole
from auto_hold_breath.aim_point import Aim_Point
from image_detect.detect import Detector
from auto_position_label.crop_position import crop_screen, screen_position as sc_pos
from screen_capture import win32_cap


def move_mouse(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx//2), int(dy//2))


class Temp_QObject(QObject):
    state_str_signal = pyqtSignal(str)


class Key_Listener(PyKeyboardEvent):
    def __init__(self, all_states, rect):
        PyKeyboardEvent.__init__(self)

        self.all_states = all_states
        self.res_list = []
        self.hole_counter = 0
        self.save_root = 'D:/github_project/auto_press_down_gun/press_gun/generate_distance'

        self.in_tab_detect = Detector('in_tab')
        self.name_detect = Detector('weapon1name')
        self.scope_detect = Detector('weapon1scope')

        self.aim_point = Aim_Point()
        self.bullet_hole = Bullet_Hole()
        self.temp_qobject = Temp_QObject()

        self.rect = rect

    def tap(self, keycode, character, press):
        if keycode == 9 and press:  # tab
            self.tab_func()

        if keycode == 82 and press:  # r
            self.hole_counter = 0

        if keycode == 162 and press:  # ctrl
            if self.all_states.weapon[0].name != '':
                self.cap_screens()

    def tab_func(self):
        screen = win32_cap('D:/github_project/auto_press_down_gun/temp_image/auto_screen_capture.png')
        if 'in' == self.in_tab_detect.match_avr_thr(crop_screen(screen, sc_pos['in_tab'])):
            n = 0
            name_crop = crop_screen(screen, sc_pos['weapon1name'])
            scope_crop = crop_screen(screen, sc_pos['weapon1scope'])
            self.all_states.weapon[n].name = self.name_detect.match_avr_thr(name_crop)
            self.all_states.weapon[n].scope = self.scope_detect.match_avr_thr(scope_crop, absent_return="1")

            self.hole_counter = 0

            self.print_state()

    def cap_screens(self):
        save_fold = os.path.join(self.save_root, self.all_states.weapon[0].name)
        os.makedirs(save_fold, exist_ok=True)

        r_x0, r_y0, r_x1, r_y1 = self.rect
        self.hole_counter = 0

        im = win32_cap(rect=(r_x0, r_y0, r_x1, r_y1))
        hole_centers = self.bullet_hole.find(im)

        x_0 = (r_x1 - r_x0) // 2
        y_0 = (r_y1 - r_y0 - 30)
        if len(hole_centers):
            x_to, y_to = hole_centers[-1]
            move_mouse(x_to-x_0, y_to-y_0)
            time.sleep(0.1)

        while True:
            print('===', self.hole_counter)
            im = win32_cap(rect=(r_x0, r_y0, r_x1, r_y1))
            hole_centers = self.bullet_hole.find(im)
            for hx, hy in hole_centers:
                cv2.circle(im, (hx, hy), 30, (255, 255, 255), thickness=2)
            cv2.imwrite(self.all_states.weapon[0].name + '/' + str(self.hole_counter) + '.png', im)
            # cv2.imshow('im', im)
            # cv2.waitKey()

            if len(hole_centers) < 2:
                break
            x_to = hole_centers[-2][0]
            y_to = hole_centers[-2][1]
            move_mouse(x_to-x_0, y_to-y_0)
            time.sleep(0.1)

            self.hole_counter += 1

    def print_state(self):
        n = self.all_states.weapon_n
        w = self.all_states.weapon[0]
        gun1_state = str(w.name) + '-' + str(w.fire_mode) + '-' + str(w.scope) + '-' + str(w.muzzle)[3:6] + '-' + str(
            w.grip)
        w = self.all_states.weapon[1]
        gun2_state = str(w.name) + '-' + str(w.fire_mode) + '-' + str(w.scope) + '-' + str(w.muzzle)[3:6] + '-' + str(
            w.grip)
        if n == 0:
            emit_str = ' * ' + gun1_state + '\n' + gun2_state
        else:
            emit_str = gun1_state + '\n' + ' * ' + gun2_state
        self.temp_qobject.state_str_signal.emit(emit_str)


if __name__ == '__main__':
    states = All_States()
    kl = Key_Listener(states)
    kl.run()


