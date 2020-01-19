# [y1, x1, y2, x2]
screen_position = \
    {'fire_mode': [1652, 1336, 1673, 1360],
     'in_tab': [1053, 138, 1096, 148],
     'in_scope': [1669, 1179, 1766, 1208],

     'weapon1name': [103, 1358, 123, 1471],
     'weapon2name': [333, 1358, 353, 1471],

     'weapon1scope': [117, 1588, 162, 1633],
     'weapon1muzzle': [250, 1316, 295, 1361],
     'weapon1grip': [250, 1418, 295, 1463],
     'weapon1magazine': [250, 1528, 295, 1573],
     'weapon1butt': [250, 1740, 295, 1785],
     'weapon2scope': [347, 1588, 392, 1633],
     'weapon2muzzle': [480, 1316, 525, 1361],
     'weapon2grip': [480, 1418, 525, 1463],
     'weapon2magazine': [480, 1528, 525, 1573],
     'weapon2butt': [480, 1740, 525, 1785]}

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
