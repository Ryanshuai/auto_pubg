import os
import time

from yaml_to_object import YamlDecoder, Cls


time.sleep(1)

now_time = time.time()
cwd = os.getcwd()

yaml_wait_list = []

for fpathe, dirs, fs in os.walk(cwd):
    for f in fs:
        if f[-5:] == '.yaml':
            yaml_file = os.path.join(fpathe, f)
            ch_time = os.stat(yaml_file).st_mtime
            if now_time - ch_time < 10:
                yaml_wait_list.append(yaml_file)

# print(yaml_wait_list)

assert len(yaml_wait_list) == 1
yaml_file = yaml_wait_list[0]
arg = YamlDecoder(yaml_file)

py_file_path = yaml_file[:-5]+'.py'


def write_down_obj(obj, father_name, tab_num):
    attr_list = dir(obj)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or callable(getattr(obj, x)) or x == ''), attr_list))

    line = "{}class {}:".format(tab_num*'    ', father_name.upper())
    lines.append(line)
    line = "{}def __init__(self):".format((tab_num+1)*'    ', father_name.upper())
    lines.append(line)

    variable_list = []
    function_list = []
    for attr in attr_list:
        if not isinstance(getattr(obj, attr), Cls):
            variable_list.append(attr)
        else:
            function_list.append(attr)

    for attr in variable_list:
        if isinstance(getattr(obj, attr), str):
            line = "{}self.{} = '{}'".format((tab_num+2)*'    ', attr, getattr(obj, attr))
            lines.append(line)
        else:
            line = "{}self.{} = {}".format((tab_num+2)*'    ', attr, getattr(obj, attr))
            lines.append(line)

    for attr in function_list:
        write_down_obj(getattr(obj, attr), attr, tab_num=tab_num+2)
        line = "{}self.{} = {}()".format((tab_num+2)*'    ', attr, attr.upper())
        lines.append(line)


lines = []
write_down_obj(arg, father_name='Arg', tab_num=0)
# for line in lines:
#     print(line)

with open(py_file_path, "w") as f:
    for line in lines:
        f.write(line)
        f.write('\n')




