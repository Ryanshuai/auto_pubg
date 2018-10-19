import yaml
import os
import time


def input_parsing(inp):
    if isinstance(inp, str):
        path = inp
        f = open(path)
        d = yaml.load(f)
    else:
        raise Exception('default input type not support')
    return d


def dic2obj(d):
    top = Cls()
    for k, v in d.items():
        if isinstance(v, dict):
            setattr(top, k, dic2obj(v))
        else:
            setattr(top, k, v)
    return top


def obj_merge(ob_0, ob_1, no_list=None):
    if no_list is None:
        no_list = []
    attr_list = dir(ob_1)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or x == 'cover_by'), attr_list))
    for attr in attr_list:
        if attr in no_list:
            continue
        if not isinstance(getattr(ob_1, attr), Cls):
            val = getattr(ob_1, attr)
            setattr(ob_0, attr, val)
        if isinstance(getattr(ob_1, attr), Cls):
            obj_merge(getattr(ob_0, attr), getattr(ob_1, attr))

    return ob_0


def obj_eq(ob_0, ob_1, no_list=None):
    if no_list is None:
        no_list = []
    attr_list = dir(ob_1)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or x == 'cover_by' or x == ''), attr_list))
    for attr in attr_list:
        if attr in no_list:
            continue
        if hasattr(ob_0, attr) ^ hasattr(ob_1, attr):
            return False
        if not isinstance(getattr(ob_0, attr), Cls):
            if getattr(ob_0, attr) != getattr(ob_1, attr):
                return False
        if isinstance(getattr(ob_0, attr), Cls):
            return obj_eq(getattr(ob_0, attr), getattr(ob_1, attr))

    return True


def is_obj_no_none(obj):
    attr_list = dir(obj)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or x == 'cover_by' or x == ''), attr_list))
    for attr in attr_list:
        if not isinstance(getattr(obj, attr), Cls):
            if getattr(obj, attr) is None:
                print(attr, 'is None!')
                return False
        else:
            if not is_obj_no_none(getattr(obj, attr)):
                print(attr, 'is None!')
                return False
    return True


def fill_in_abs_path(obj):
    attr_list = dir(obj)
    if 'root' in attr_list:
        relative_path_attr_list = list(filter(lambda x: x[:9] == 'relative_', attr_list))
        for attr in relative_path_attr_list:
            # if getattr(obj, attr[9:]) is None:
                assert getattr(obj, 'root') is not None, '{}.root cannot be None'.format(attr)
                abs_path = os.path.join(getattr(obj, 'root'), getattr(obj, attr))
                setattr(obj, attr[9:], abs_path)
    for attr in attr_list:
        if isinstance(getattr(obj, attr), Cls):
            fill_in_abs_path(getattr(obj, attr))


class Cls:
    def __init__(self):
        pass

    def __eq__(self, other):
        return obj_eq(self, other)

    def __ne__(self, other):
        return not obj_eq(self, other)

    def _fill_in_stamp(self, config_file):
        self.stamp.config_name = os.path.basename(config_file)
        user_list = list(filter(lambda user: os.path.exists('/root/' + user), ['qxc', 'ysy', 'jh1', 'ys2', 'qty']))
        if len(user_list) == 0:
            user_list = list(filter(lambda user: os.path.exists('/home/' + user), ['qxc', 'ysy', 'jh1', 'ys', 'qty']))
        self.stamp.user = user_list[0]
        self.stamp.time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        self.stamp.experiment_name = self.stamp.user + '-' + self.stamp.config_name + '-' + self.stamp.time

    def _fill_in_save_root(self):
        self.save.root = os.path.join(self.save.root_ , self.stamp.experiment_name)
        # self.save.root =  os.path.join(self.save.root_ , self.stamp.user, self.stamp.experiment_name)

    def _fill_in_abs_path(self):
        fill_in_abs_path(self)

    def cover_by(self, specific_file, no_list=None):
        ds = input_parsing(specific_file)
        obj_ds = dic2obj(ds)
        obj_merge(self, obj_ds, no_list=no_list)
        self._fill_in_stamp(specific_file)
        self._fill_in_save_root()
        self._fill_in_abs_path()

    def set_experiment_name(self, experiment_name):
        self.stamp.experiment_name = experiment_name
        self._fill_in_save_root()
        self._fill_in_abs_path()

    def set_profile_name(self, profile_name):
        self._fill_in_stamp(profile_name)
        self._fill_in_save_root()
        self._fill_in_abs_path()


class YamlDecoder(object):
    def __new__(cls, default_file, specific_file=None):
        d = input_parsing(default_file)
        obj = dic2obj(d)

        if specific_file is not None:
            ds = input_parsing(specific_file)
            obj_ds = dic2obj(ds)
            obj = obj_merge(obj, obj_ds)

        obj._fill_in_stamp(default_file if specific_file is None else specific_file)
        obj._fill_in_save_root()
        obj._fill_in_abs_path()
        assert is_obj_no_none(obj)

        return obj



