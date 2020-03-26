import threading
from pynput import keyboard, mouse
from PyQt5.QtCore import pyqtSignal, QObject

from image_detection.detect import Detector
from calibrate_icons.get_position.position_constant import crop_position
from all_states import All_States
from press_gun.press import Press
from screen_capture import win32_cap


class Temp_QObject(QObject):
    state_str_signal = pyqtSignal(str)


class Key:
    def __init__(self, all_states):
        self.all_states = all_states
        self.screen = None
        self.in_block = False
        self.in_right = False

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

        self.temp_qobject = Temp_QObject()
        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)

    def on_press(self, key):
        if key == keyboard.Key.tab:
            import time
            time.sleep(0.2)
            self.screen = win32_cap()
            threading.Timer(0.00001, self.tab_func).start()

        if key == keyboard.Key.f12:
            self.all_states.dont_press = True
        key = str(key)
        if key == 'g' or key == '5':
            self.all_states.dont_press = True

        if key == 'b':
            self.all_states.dont_press = False
            threading.Timer(0.5, self.set_fire_mode).start()

        if key == '1':
            self.all_states.set_weapon_n(0)
            self.print_state()
            # threading.Timer(0.5, self.set_fire_mode).start()

        if key == '2':
            self.all_states.set_weapon_n(1)
            self.print_state()
            # threading.Timer(0.5, self.set_fire_mode).start()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed and (not self.all_states.dont_press):
            print(2222)
            n = self.all_states.weapon_n
            if self.all_states.weapon[n].fire_mode in ['full', '']:
                print(self.all_states.weapon[n].dist_seq)
                print(self.all_states.weapon[n].time_seq)
                self.press = Press(self.all_states.weapon[n].dist_seq, self.all_states.weapon[n].time_seq)
                self.press.start()

        if button == mouse.Button.left and (not pressed) and (not self.all_states.dont_press):
            if hasattr(self, 'press'):
                self.press.stop()

    def tab_func(self):
        if 'type' == self.in_tab_detect.detect(get_crop('in-tab', self.screen)):

            position_filtered = dict(filter(lambda x: ('gun' in x[0]), crop_position.items()))
            for position, (y1, x1, y2, x2) in position_filtered.items():
                corp_im = self.screen[y1:y2, x1:x2]
                pos = position.split('_')[-1]
                crop_name = self.gun_detector[pos].detect(corp_im)
                if '1' in position:
                    self.all_states.weapon[0].set(pos, crop_name)
                if '2' in position:
                    self.all_states.weapon[1].set(pos, crop_name)

            self.all_states.weapon[0].fire_mode = 'full'
            self.all_states.weapon[0].name = 'm762'
            self.all_states.weapon[0].type = 'ar'

            self.all_states.weapon[0].set_seq()
            self.all_states.weapon[1].set_seq()
            self.print_state()

            # self.all_states.set_screen_state('3p')
            # threading.Timer(0.5, self.set_fire_mode).start()

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


def get_screen(name):
    pos = crop_position[name]
    im = win32_cap(filename='temp_image', rect=pos)
    return im


if __name__ == '__main__':
    all_states = All_States()
    k = Key(all_states)
    k.key_listener.run()
