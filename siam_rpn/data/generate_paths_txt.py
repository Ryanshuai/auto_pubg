import os
from config.siam_rpn.default import ARG
from config.siam_rpn.default_ys2_ubuntu import ARG as ys_ARG
from data.xml_2_dict import xml_2_dict


if os.path.exists('/home/'):
    arg = ys_ARG()
    print('ys_arg')
else:
    arg = ARG()
    print('server_arg')

root_path = arg.data.dataset.train.root_path

img_r_path = arg.data.dataset.train.data_path
xml_r_path = arg.data.dataset.train.annotation_path

img_dir = os.path.join(root_path, img_r_path)
xml_dir = os.path.join(root_path, xml_r_path)


relative_path_list = []
for dir1 in os.listdir(xml_dir):
    dir1_path = os.path.join(xml_dir, dir1)
    for dir2 in os.listdir(dir1_path):
        dir2_path = os.path.join(dir1_path, dir2)
        # item_num = len(os.listdir(dir2_path))
        relative_img_path = os.path.join(img_r_path, dir1, dir2)
        relative_xml_path = os.path.join(xml_r_path, dir1, dir2)
        line = relative_img_path+' '+relative_xml_path+'\n'
        append_flag = True
        # for itm in os.listdir(dir2_path):
        #     itm_path = os.path.join(dir2_path, itm)
        #     xml_dict = xml_2_dict(itm_path)
        #     if 'object' not in xml_dict:
        #         append_flag = False

        if append_flag:
            relative_path_list.append(line)
            print(line)
        else:
            print('not append:', line)


with open('relative_paths.txt', 'w') as f:
    f.writelines(relative_path_list)