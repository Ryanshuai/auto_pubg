from calibrate_distance.write_dict import write_to_file, write_to_file_abs
from calibrate_distance.gun_distance_constant import dist_lists

# write_to_file(dist_lists, 'gun_distance_constant.py')
soldier76_dist = {
    'vector':
        [
            [1, 0],
            [5, 52],
            [10, 72],
            [15, 90],
            [25, 122],
            [33, 124],
        ],

    'g36c':
        [
            [1, 0],
            [2, 135],
            [5, 62],
            [10, 80],
            [20, 101],
            [25, 108],
            [40, 109],
        ],
    'scar':
        [
            [1, 0],
            [2, 140],
            [3, 40],
            [4, 60],
            [5, 80],
            [10, 94],
            [15, 102],
            [40, 122],
        ],

    'm762':
        [
            [1, 0],
            [2, 140],
            [5, 81],
            [7, 123],
            [10, 143],
            [11, 188],
            [12, 180],
            [15, 188],
            [20, 190],
            [25, 197],
            [40, 191],
        ],
    'akm':
        [
            [1, 0],
            [2, 149],
            [5, 93],
            [10, 104],
            [15, 140],
            [25, 145],
            [35, 146],
            [40, 147],
        ],
}

factor = 0.25
for name, pairs in soldier76_dist.items():
    if name == 'm416':
        continue
        factor *= 1 / 0.85 * 1 / 0.85
    elif name == 'ump45':
        continue
        factor *= 1
    elif name == 'vector':
        continue
        factor *= 1
    elif name == 'tommy':
        continue
        factor *= 1
    elif name == 'uzi':
        continue
        factor *= 1
    else:
        factor *= 1 / 0.85

    new_list = list()
    last_i = 1
    for i, dist in pairs:
        new_list += [dist * factor] * (i - last_i)
        last_i = i

    write_to_file_abs(gun_name=name, new_dist=new_list)
