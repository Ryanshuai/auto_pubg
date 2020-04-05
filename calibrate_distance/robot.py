import os
import threading
from pynput import keyboard, mouse
from PyQt5.QtCore import pyqtSignal, QObject

from image_detection.detect import Detector
from calibrate_icons.get_position.position_constant import crop_position
from all_states import All_States
from screen_capture import win32_cap
from calibrate_distance.press import Press
from press_gun.time_periods_constant import time_periods


class Temp_QObject(QObject):
    state_str_signal = pyqtSignal(str)


class Robot:
    def __init__(self, all_states):
        self.all_states = all_states
        self.screen = None
        self.in_block = False

        self.fire_mode_detect = Detector('fire-mode', 'white')
        self.in_tab_detect = Detector('in-tab', 'white')
        self.posture_detect = Detector('posture', 'white')
        # self.in_scope_detect = Detector('in_scope')

        self.gun_detector = dict()
        self.gun_detector['name'] = Detector('name', 'white')
        self.gun_detector['scope'] = Detector('scope', 'icon', '1')
        self.gun_detector['muzzle'] = Detector('muzzle', 'icon')
        self.gun_detector['grip'] = Detector('grip', 'icon')
        self.gun_detector['butt'] = Detector('butt', 'icon')
        # self.gun_detector['magazine'] = Detector('magazine', 'icon')

        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.key_control = keyboard.Controller()
        self.key_listener.start()
        self.mouse_listener.start()

        self.temp_qobject = Temp_QObject()
        os.makedirs('calibrate_distance/image_match_dir', exist_ok=True)
        self.gun_name_dir = ''
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        if key == keyboard.Key.tab:
            self.screen = win32_cap()
            threading.Timer(0.3, self.is_in_tab).start()
        if key == keyboard.Key.f12:
            self.all_states.dont_press = True

        if key == keyboard.Key.ctrl_l:
            for i in range(100):
                if not os.path.exists(self.gun_name_dir + str(i)):
                    os.makedirs(self.gun_name_dir + str(i))
                    self.image_dir = self.gun_name_dir + str(i) + '/'
                    break
            win32_cap(filename=self.image_dir + '0.png', rect=(100, 100, 400, 1600))


        if hasattr(key, 'char'):
            key = key.char
        if key == 'g' or key == '5':
            self.all_states.dont_press = True
        if key == 'b':
            self.all_states.dont_press = False
            threading.Timer(0.5, self.set_fire_mode).start()
        if key == '1' or key == '2':
            self.all_states.dont_press = False
            self.all_states.set_weapon_n(int(key) - 1)
            threading.Timer(0.5, self.set_fire_mode).start()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed and (not self.all_states.dont_press):
            if not self.all_states.dont_press:
                n = self.all_states.weapon_n
                if self.all_states.weapon[n].type in ['ar', 'smg', 'mg']:
                    time_interval = time_periods[self.all_states.weapon[n].name]
                    self.press = Press(time_interval, image_dir=self.image_dir)
                    self.press.start()
                elif self.all_states.weapon[n].type == 'dmr':
                    time_interval = 0.1
                    self.press = Press(time_interval, length=5, image_dir=self.image_dir)
                    self.press.start()
        if button == mouse.Button.left and (not pressed) and (not self.all_states.dont_press):
            if hasattr(self, 'press'):
                self.press.stop()
            if self.all_states.screen_state == 'tab':
                threading.Timer(0.0001, self.tab_func).start()

        if button == mouse.Button.right and (not pressed):
            if self.all_states.screen_state == 'tab':
                threading.Timer(0.0001, self.tab_func).start()

    def is_in_tab(self):
        if 'type' == self.in_tab_detect.detect(get_screen('in-tab')):
            self.all_states.screen_state = 'tab'
        else:
            self.all_states.screen_state = 'default'
            threading.Timer(0.5, self.set_fire_mode).start()

    def tab_func(self):
        self.screen = get_screen()
        position_filtered = dict(filter(lambda x: ('gun' in x[0]), crop_position.items()))
        for position, (y1, x1, y2, x2) in position_filtered.items():
            corp_im = self.screen[y1:y2, x1:x2]
            pos = position.split('_')[-1]
            crop_name = self.gun_detector[pos].detect(corp_im)
            if '1' in position:
                self.all_states.weapon[0].set(pos, crop_name)
            if '2' in position:
                self.all_states.weapon[1].set(pos, crop_name)

            self.print_state()
            n = self.all_states.weapon_n
            gun_name = self.all_states.weapon[n].name

            os.makedirs('calibrate_distance/image_match_dir/' + gun_name + '/', exist_ok=True)
            self.gun_name_dir = 'calibrate_distance/image_match_dir/' + gun_name + '/'

    def set_fire_mode(self):
        fire_mode_crop = get_screen('fire-mode')
        fire_mode = self.fire_mode_detect.detect(fire_mode_crop)
        n = self.all_states.weapon_n
        self.all_states.weapon[n].set('fire-mode', fire_mode)
        self.print_state()

    def print_state(self):
        w = self.all_states.weapon[0]
        gun1_state = str(w.name) + '-' + str(w.fire_mode) + '-' + str(w.scope) + '-' + str(w.muzzle)[3:6] + '-' + str(
            w.grip)
        w = self.all_states.weapon[1]
        gun2_state = str(w.name) + '-' + str(w.fire_mode) + '-' + str(w.scope) + '-' + str(w.muzzle)[3:6] + '-' + str(
            w.grip)
        if self.all_states.weapon_n == 0:
            emit_str = ' * ' + gun1_state + '\n' + gun2_state
        else:
            emit_str = gun1_state + '\n' + ' * ' + gun2_state
        self.temp_qobject.state_str_signal.emit(emit_str)


def get_crop(name, screen):
    y1, x1, y2, x2 = crop_position[name]
    corp_im = screen[y1:y2, x1:x2]
    return corp_im


def get_screen(name=None):
    if name is None:
        return win32_cap(filename='temp_image')
    pos = crop_position[name]
    return win32_cap(filename='temp_image', rect=pos)


if __name__ == '__main__':
    all_states = All_States()
    k = Robot(all_states)
    k.key_listener.run()
