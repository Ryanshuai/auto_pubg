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


for dir1 in os.listdir(xml_dir):
    dir1_path = os.path.join(xml_dir, dir1)
    for dir2 in os.listdir(dir1_path):
        dir2_path = os.path.join(dir1_path, dir2)
        for item in os.listdir(dir2_path):
            end_path = os.path.join(dir1, dir2, item)
            xml_path = os.path.join(xml_dir, end_path)
            xml_dict = xml_2_dict(xml_path)
            if 'object' not in xml_dict:
                img_path = os.path.join(img_dir, end_path[0:-4]+'.JPEG')

                print('remove:'+xml_path)
                print('remove:'+img_path)
                os.remove(xml_path)
                os.remove(img_path)

