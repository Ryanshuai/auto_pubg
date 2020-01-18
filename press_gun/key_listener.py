import threading
from pykeyboard import PyKeyboardEvent
from PyQt5.QtCore import pyqtSignal, QObject

from image_detect.detect import Detector
from auto_position_label.crop_position import screen_position
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

        self.fire_mode_detect = Detector('fire_mode')
        self.in_tab_detect = Detector('in_tab')
        self.in_scope_detect = Detector('in_scope')

        self.weapon1name_detect = Detector('weapon1name')
        self.weapon1scope_detect = Detector('weapon1scope')
        self.weapon1muzzle_detect = Detector('weapon1muzzle')
        self.weapon1grip_detect = Detector('weapon1grip')
        self.weapon1butt_detect = Detector('weapon1butt')

        self.weapon2name_detect = Detector('weapon2name')
        self.weapon2scope_detect = Detector('weapon2scope')
        self.weapon2muzzle_detect = Detector('weapon2muzzle')
        self.weapon2grip_detect = Detector('weapon2grip')
        self.weapon2butt_detect = Detector('weapon2butt')

        self.temp_qobject = Temp_QObject()

    def tap(self, keycode, character, press):
        if keycode == 9 and press:  # tab
            if self.in_block:
                return
            self.in_block = True
            threading.Timer(0.1, self.no_block).start()

            self.screen = win32_cap()
            threading.Timer(0.001, self.tab_func).start()

        if keycode == 66 and press:  # b
            self.all_states.dont_press = False
            threading.Timer(0.5, self.b_func).start()

        if keycode == 49 and press:  # 1
            n_change = self.all_states.set_weapon_n(0)
            if n_change:
                self.print_state()

        if keycode == 50 and press:  # 2
            n_change = self.all_states.set_weapon_n(1)
            if n_change:
                self.print_state()

        if keycode == 188 and press:  # ,
            if not self.all_states.dont_press:
                n = self.all_states.weapon_n
                self.press = Press(self.all_states.weapon[n].dist_seq, self.all_states.weapon[n].time_seq)
                self.press.start()

        if keycode == 190 and press:  # .
            if not self.all_states.dont_press:
                if self.press.is_alive():
                    self.press.stop()

        if (keycode == 123 or keycode == 71 or keycode == 53) and press:  # F12 g 5
            self.all_states.dont_press = True

        if keycode == 219 and press:  # [
            self.all_states.dont_press = True

        if keycode == 221 and press:  # ]
            self.all_states.dont_press = False

    def escape(self, event):
        return False

    def no_block(self):
        self.in_block = False

    def tab_func(self):
        self.all_states.dont_press = True
        if 'in' == self.in_tab_detect.match_avr_thr(get_screen('in_tab')):
            self.all_states.dont_press = False

            crop = crop_screen(self.screen, 'weapon1name')
            res = self.weapon1name_detect.match_avr_thr(crop)
            w1n_change = self.all_states.weapon[0].set_name(res)

            crop = crop_screen(self.screen, 'weapon1scope')
            res = self.weapon1scope_detect.match_avr_thr(crop, absent_return="1")
            w1s_change = self.all_states.weapon[0].set_scope(res)

            crop = crop_screen(self.screen, 'weapon1muzzle')
            res = self.weapon1muzzle_detect.match_avr_thr(crop)
            w1m_change = self.all_states.weapon[0].set_muzzle(res)

            crop = crop_screen(self.screen, 'weapon1grip')
            res = self.weapon1grip_detect.match_avr_thr(crop)
            self.grip = self.all_states.weapon[0].set_grip(res)
            w1g_change = self.grip

            crop = crop_screen(self.screen, 'weapon1butt')
            res = self.weapon1butt_detect.match_avr_thr(crop)
            w1b_change = self.all_states.weapon[0].set_butt(res)

            crop = crop_screen(self.screen, 'weapon2name')
            res = self.weapon2name_detect.match_avr_thr(crop)
            w2n_change = self.all_states.weapon[1].set_name(res)

            crop = crop_screen(self.screen, 'weapon2scope')
            res = self.weapon2scope_detect.match_avr_thr(crop, absent_return="1")
            w2s_change = self.all_states.weapon[1].set_scope(res)

            crop = crop_screen(self.screen, 'weapon2muzzle')
            res = self.weapon2muzzle_detect.match_avr_thr(crop)
            w2m_change = self.all_states.weapon[1].set_muzzle(res)

            crop = crop_screen(self.screen, 'weapon2grip')
            res = self.weapon2grip_detect.match_avr_thr(crop)
            w2g_change = self.all_states.weapon[1].set_grip(res)

            crop = crop_screen(self.screen, 'weapon2butt')
            res = self.weapon2butt_detect.match_avr_thr(crop)
            w2b_change = self.all_states.weapon[1].set_butt(res)

            if w1n_change or w1s_change or w1m_change or w1g_change or w1b_change:
                self.all_states.weapon[0].set_seq()
            if w2n_change or w2s_change or w2m_change or w2g_change or w2b_change:
                self.all_states.weapon[1].set_seq()

            self.print_state()

    def b_func(self):
        fire_mode_crop = get_screen('fire_mode')
        fire_mode = self.fire_mode_detect.match_white(fire_mode_crop)
        n = self.all_states.weapon_n
        self.all_states.weapon[n].set_fire_mode(fire_mode)

        self.print_state()

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


def get_screen(name):
    pos = screen_position[name]
    temp_fold = 'D:/github_project/auto_press_down_gun/press_gun/temp_image/'
    im = win32_cap(temp_fold + name + '.png', pos)
    return im


def crop_screen(screen, name):
    rect = screen_position[name]
    x0, y0, x1, y1 = rect
    im = screen[y0:y1, x0:x1, :]
    return im


if __name__ == '__main__':
    all_states = All_States()
    k = Key_Listener(all_states)
    k.run()
