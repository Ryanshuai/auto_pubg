import math
from press_gun.time_periods_constant import time_periods
from calibrate_distance.gun_distance_constant import dist_lists

all_guns = ['98k', 'm24', 'awm', 'mini14', 'mk14', 'qbu', 'sks', 'slr', 'vss', 'akm', 'aug', 'groza', 'm416', 'qbz',
            'scar', 'm762', 'g36c', 'm16', 'mk47', 'tommy', 'uzi', 'ump45', 'vector', 'pp19', 'm249', 'dp28', 's12k',
            's1987', 's686', 'win94', ]

single_guns = ['98k', 'awm', 'm16', 'm24', 'mini14', 's12k', 's1987', 's686', 'sks', 'slr', 'win94', ]
full_guns = ['dp28', 'm249', ]
single_burst_guns = ['m16', 'mk47', ]
single_full_guns = ['akm', 'aug', 'groza', 'm416', 'qbz', 'scar', 'mk14', 'tommy', 'uzi', 'vss', ]
single_burst_full_guns = ['m762', 'ump45', 'vector', ]
can_full_guns = ['akm', 'aug', 'groza', 'm416', 'qbz', 'scar', 'mk14', 'tommy', 'uzi', 'vss', 'm762', 'ump45', 'vector',
                 'dp28', 'm249', 'pp19', 'g36c', ]

SPs = ['98k', 'm24', 'awm', ]
DMRs = ['mini14', 'mk14', 'qbu', 'sks', 'slr', 'vss', ]
ARs = ['akm', 'aug', 'groza', 'm416', 'qbz', 'scar', 'm762', 'g36c', 'm16', 'mk47', ]
SMGs = ['tommy', 'uzi', 'ump45', 'vector', 'pp19', ]
MGs = ['m249', 'dp28', ]
shotguns = ['s12k', 's1987', 's686', ]

bullet_762_guns = ['98k', 'm24', 'mk14', 'sks', 'slr', 'akm', 'groza', 'm762', 'mk47', 'dp28', ]
bullet_556_guns = ['mini14', 'qbu', 'aug', 'm416', 'qbz', 'scar', 'g36c', 'm16', ]
bullet_9_guns = ['vss', 'uzi', 'vector', 'pp19', ]
bullet_45_guns = ['tommy', 'ump45', 'win94', ]
bullet_12_guns = ['s12k', 's1987', 's686', ]
bullet_300_guns = ['awm', ]


def factor_scope(scope):
    factor = 1
    if scope == 1:
        factor = 1.
    if scope == 2:
        factor = 1
    if scope == 3:
        factor = 1
    if scope == 4:
        factor = 1.1
    if scope == 6:
        factor = 0.8
    return scope * factor


def calculate_press_seq(name, scope_factor):
    scope_factor = factor_scope(scope_factor)
    dist_interval = dist_lists.get(name, [])
    dist_interval = [i * scope_factor for i in dist_interval]
    time_interval = time_periods.get(name, 1)
    divide_num0 = math.floor(time_interval / 0.01)  # 整数分割
    time_sequence = list()
    dist_sequence = list()
    for dist in dist_interval:
        divide_num1 = math.floor(dist / 3)  # 整数分割
        divide_num = min(divide_num0, divide_num1)
        for i in range(divide_num):
            time_sequence.append(time_interval / divide_num)
            dist_sequence.append(dist // divide_num)
        dist_sequence[-1] += dist % divide_num

    return dist_sequence, time_sequence


# def calculate_press_seq(name, all_factor):
#     dist_interval = dist_lists.get(name, [])
#     dist_interval = [i * all_factor for i in dist_interval]
#     time_interval = time_periods.get(name, 1)
#
#     time_sequence = list()
#     dist_sequence = list()
#     for dist in dist_interval:
#         divide_num = math.floor(dist/10)  # 整数分割
#         for i in range(divide_num):
#             time_sequence.append(time_interval / divide_num)
#             dist_sequence.append(10)
#         dist_sequence[-1] += dist % 10
#
#     return dist_sequence, time_sequence


class Ground():
    pass


class Back():
    pass


class Weapon():
    def __init__(self):
        self.fire_mode = 'single'
        self.name = ''
        self.scope = '1'
        self.muzzle = ''
        self.grip = ''
        self.butt = ''

        self.all_factor = 1
        self.scope_factor = 1
        self.muzzle_factor = 1
        self.grip_factor = 1
        self.butt_factor = 1

        self.dist_seq = list()
        self.time_seq = list()

    def set_fire_mode(self, fire_mode):
        if self.fire_mode == fire_mode:
            return False
        self.fire_mode = fire_mode
        return True

    def set_name(self, name):
        if self.name == name:
            return False
        self.name = name
        return True

    def set_scope(self, scope):
        if self.scope == scope:
            return False
        self.scope = scope
        self.scope_factor = int(scope.replace('r', '').replace('h', ''))
        self.scope_factor = factor_scope(self.scope_factor)
        if self.name == 'vss':
            self.scope_factor = 4
        return True

    def set_muzzle(self, muzzle):
        if self.muzzle == muzzle:
            return False
        self.muzzle = muzzle
        if self.muzzle.endswith('flash'):
            self.muzzle_factor = 0.9

        elif self.muzzle.endswith('suppressor'):  # 消音
            self.muzzle_factor = 1.0

        elif self.muzzle.endswith('compensator'):
            if self.name in ARs:
                self.muzzle_factor = 0.85
            elif self.name in SMGs:
                self.muzzle_factor = 0.75
            elif self.name in SPs:
                self.muzzle_factor = 0.8
        elif self.grip == '':
            self.muzzle_factor = 1.0
        return True

    def set_grip(self, grip):
        if self.grip == grip:
            return False
        self.grip = grip
        if self.grip == 'thumb':
            self.grip_factor = 0.85
        elif self.grip == 'lightweight':
            self.grip_factor = 1.25
        elif self.grip == 'half':
            self.grip_factor = 0.9
        elif self.grip == 'angled':
            self.grip_factor = 1.0
        elif self.grip == 'vertical':
            self.grip_factor = 0.85
        elif self.grip == '':
            self.grip_factor = 1.0
        return True

    def set_butt(self, butt):
        if self.butt == butt:
            return False
        if self.name == 'm416' and butt == 'm416_butt':
            self.butt_factor = 0.85
        self.butt = butt
        if self.butt == '':
            self.butt_factor = 1.0
        return True

    def set_seq(self):
        self.all_factor = self.scope_factor * self.muzzle_factor * self.grip_factor * self.butt_factor
        self.dist_seq, self.time_seq = calculate_press_seq(self.name, self.all_factor)


class All_States():
    def __init__(self):
        self.dont_press = False
        self.in_scope = False

        self.weapon_n = 0
        self.weapon = [Weapon(), Weapon()]

        self.hm = None
        self.bp = None
        self.vt = None

    def set_weapon_n(self, weapon_n):
        original_n = self.weapon_n
        self.weapon_n = weapon_n
        return original_n != weapon_n


if __name__ == '__main__':
    states = All_States()
