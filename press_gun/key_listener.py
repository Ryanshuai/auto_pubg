import threading
from pykeyboard import PyKeyboardEvent
from PyQt5.QtCore import pyqtSignal, QObject

from image_detection.detect import Detector
from calibrate_icons.get_position.position_constant import crop_position
from all_states import All_States
from press_gun.press import Press
from screen_capture import win32_cap


class Temp_QObject(QObject):
    state_str_signal = pyqtSignal(str)


class Key_Listener(PyKeyboardEvent):
    def __init__(self, all_states):
        PyKeyboardEvent.__init__(self)

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

    def tap(self, keycode, character, press):
        if keycode == 9 and press:  # tab
            self.screen = win32_cap()
            threading.Timer(0.00001, self.tab_func).start()

        if keycode == 66 and press:  # b
            self.all_states.dont_press = False
            threading.Timer(0.5, self.set_fire_mode).start()

        if keycode == 49 and press:  # 1
            self.all_states.set_weapon_n(0)
            self.print_state()
            # threading.Timer(0.5, self.set_fire_mode).start()

        if keycode == 50 and press:  # 2
            self.all_states.set_weapon_n(1)
            self.print_state()
            # threading.Timer(0.5, self.set_fire_mode).start()

        if (keycode == 123 or keycode == 71 or keycode == 53) and press:  # F12 g 5
            self.all_states.dont_press = True

        if keycode == 188 and press:  # ,
            if not self.all_states.dont_press:
                n = self.all_states.weapon_n
                if self.all_states.weapon[n].fire_mode in ['full', '']:
                    self.press = Press(self.all_states.weapon[n].dist_seq, self.all_states.weapon[n].time_seq)
                    self.press.start()

        if keycode == 190 and press:  # .
            if not self.all_states.dont_press:
                if hasattr(self, 'press'):
                    self.press.stop()

        # if keycode == 219 and press:  # [
        #     if self.posture_detect.detect(get_screen('posture')) in ['stand', 'kneel', 'creep']:
        #         self.all_states.dont_press = False
        #     else:
        #         self.all_states.dont_press = True

        # if keycode == 221 and press:  # ]
        #     self.all_states.dont_press = False

    def escape(self, event):
        return False

    def tab_func(self):
        self.all_states.dont_press = True
        if 'time' == self.in_tab_detect.detect(get_crop('in-tab', self.screen)):
            self.all_states.dont_press = False

            position_filtered = dict(filter(lambda x: ('gun' in x[0]), crop_position.items()))
            for position, (y1, x1, y2, x2) in position_filtered.items():
                corp_im = self.screen[y1:y2, x1:x2]
                pos = position.split('_')[-1]
                crop_name = self.gun_detector[pos].detect(corp_im)
                if '1' in position:
                    self.all_states.weapon[0].set(pos, crop_name)
                if '2' in position:
                    self.all_states.weapon[1].set(pos, crop_name)

            self.all_states.weapon[0].set_seq()
            self.all_states.weapon[1].set_seq()
            self.print_state()

            # self.all_states.set_screen_state('3p')
            threading.Timer(0.5, self.set_fire_mode).start()

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
    k = Key_Listener(all_states)
    k.run()
