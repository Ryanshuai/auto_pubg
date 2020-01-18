screen_position = \
    {'fire_mode': [1652, 1336, 1673, 1360],
     'in_tab': [1053, 138, 1096, 148],
     'in_scope': [1669, 1179, 1766, 1208],

     'weapon1name': [2245, 135, 2400, 160],
     'weapon2name': [2245, 442, 2400, 467],

     'weapon1scope': [1588, 117, 1633, 162],
     'weapon1muzzle': [1316, 250, 1361, 295],
     'weapon1grip': [1418, 250, 1463, 295],
     'weapon1magazine': [1528, 250, 1573, 295],
     'weapon1butt': [1740, 250, 1785, 295],
     'weapon2scope': [1588, 347, 1633, 392],
     'weapon2muzzle': [1316, 480, 1361, 525],
     'weapon2grip': [1418, 480, 1463, 525],
     'weapon2magazine': [1528, 480, 1573, 525],
     'weapon2butt': [1740, 480, 1785, 525]
     }

screen_position_states = \
    {'fire_mode': ['single', 'burst2', 'burst3', 'full'],
     'small_fire_mode': ['single', 'burst', 'full'],
     'in_tab': ['in'],
     'in_scope': ['in'],
     'weapon1name': ['98k', 'm24', 'awm', 'mini14', 'mk14', 'qbu', 'sks', 'slr', 'vss', 'akm', 'aug', 'groza', 'm416',
                     'qbz', 'scar', 'm762', 'g36c', 'm16', 'mk47', 'tommy', 'uzi', 'ump45', 'vector', 'pp19', 'm249',
                     'dp28', 's12k', 's1987', 's686', 'win94', ],
     'weapon2name': ['98k', 'm24', 'awm', 'mini14', 'mk14', 'qbu', 'sks', 'slr', 'vss', 'akm', 'aug', 'groza', 'm416',
                     'qbz', 'scar', 'm762', 'g36c', 'm16', 'mk47', 'tommy', 'uzi', 'ump45', 'vector', 'pp19', 'm249',
                     'dp28', 's12k', 's1987', 's686', 'win94', ],
     'weapon1scope': ['1r', '1h', '2', '3', '4', '6', '8', '15'],
     'weapon2scope': ['1r', '1h', '2', '3', '4', '6', '8', '15'],
     'weapon1muzzle': ['ar_flash', 'ar_suppressor', 'ar_compensator', 'smg_flash', 'smg_suppressor', 'smg_compensator',
                       'sp_flash', 'sp_suppressor', 'sp_compensator'],
     'weapon2muzzle': ['ar_flash', 'ar_suppressor', 'ar_compensator', 'smg_flash', 'smg_suppressor', 'smg_compensator',
                       'sp_flash', 'sp_suppressor', 'sp_compensator'],
     'weapon1grip': ['thumb', 'lightweight', 'half', 'angled', 'vertical'],
     'weapon2grip': ['thumb', 'lightweight', 'half', 'angled', 'vertical'],
     'weapon1butt': ['m416_butt'],
     'weapon2butt': ['m416_butt'],
     'weapon1magazine': [],
     'weapon2magazine': [],
     'helmet': [],
     'armor': [],
     'backpack': [],
     'ground0': [],
     'ground1': [],
     'ground2': [],
     'ground3': [],
     'ground4': [],
     'ground5': [],
     'ground6': [],
     'ground7': [],
     'ground8': [],
     'ground9': [],
     'ground10': [],
     'ground11': [],
     'ground12': []
     }


def crop_screen(screen, pos):
    x0, y0, x1, y1 = pos
    return screen[y0:y1, x0:x1, :]
