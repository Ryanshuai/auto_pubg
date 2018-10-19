class ARG:
    def __init__(self):
        self.device = 'cuda'
        self.device_ids = [0]
        self.loss = 1
        class DATA:
            def __init__(self):
                class DATALOADER:
                    def __init__(self):
                        class TEST:
                            def __init__(self):
                                self.batch_size = 1
                                self.num_workers = 4
                                self.shuffle = True
                        self.test = TEST()
                        class TRAIN:
                            def __init__(self):
                                self.batch_size = 1
                                self.num_workers = 1
                                self.shuffle = True
                        self.train = TRAIN()
                        class VALID:
                            def __init__(self):
                                self.batch_size = 1
                                self.num_workers = 4
                                self.shuffle = True
                        self.valid = VALID()
                self.dataloader = DATALOADER()
                class DATASET:
                    def __init__(self):
                        class DEFAULTS:
                            def __init__(self):
                                self.annotation_path = 'Annotations/VID/train'
                                self.data_path = 'Data/VID/train'
                                self.root_path = '/home/ys/Data/ILSVRC'
                        self.defaults = DEFAULTS()
                        class TRAIN:
                            def __init__(self):
                                self.annotation_path = 'Annotations/VID/train'
                                self.data_path = 'Data/VID/train'
                                self.root_path = '/home/ys/Data/ILSVRC'
                        self.train = TRAIN()
                        class VALID:
                            def __init__(self):
                                self.annotation_path = 'Annotations/VID/train'
                                self.data_path = 'Data/VID/train'
                                self.root_path = '/home/ys/Data/ILSVRC'
                        self.valid = VALID()
                self.dataset = DATASET()
        self.data = DATA()
        class MODEL:
            def __init__(self):
                self.anchor_num = 5
                self.res_size = 17
                self.u_size = 255
                self.z_size = 127
        self.model = MODEL()
        class OPTIM:
            def __init__(self):
                self.lr = 1e-06
                self.weight_decay = 1e-05
        self.optim = OPTIM()
        class SAVE:
            def __init__(self):
                self.analyze = '/home/ys/Data/pose_estimate_save/ys-default_ys2_ubuntu.yaml-2018_10_17_17_32_14/valid/coco_analyze'
                self.model = '/home/ys/Data/pose_estimate_save/ys-default_ys2_ubuntu.yaml-2018_10_17_17_32_14/models'
                self.relative_analyze = 'valid/coco_analyze'
                self.relative_model = 'models'
                self.relative_tensorboard = 'tensorboard'
                self.relative_test = 'tst'
                self.relative_train = 'train'
                self.relative_valid = 'valid'
                self.root = '/home/ys/Data/pose_estimate_save/ys-default_ys2_ubuntu.yaml-2018_10_17_17_32_14'
                self.root_ = '/home/ys/Data/pose_estimate_save/'
                self.tensorboard = '/home/ys/Data/pose_estimate_save/ys-default_ys2_ubuntu.yaml-2018_10_17_17_32_14/tensorboard'
                self.test = '/home/ys/Data/pose_estimate_save/ys-default_ys2_ubuntu.yaml-2018_10_17_17_32_14/tst'
                self.train = '/home/ys/Data/pose_estimate_save/ys-default_ys2_ubuntu.yaml-2018_10_17_17_32_14/train'
                self.valid = '/home/ys/Data/pose_estimate_save/ys-default_ys2_ubuntu.yaml-2018_10_17_17_32_14/valid'
        self.save = SAVE()
        class STAMP:
            def __init__(self):
                self.config_name = 'default_ys2_ubuntu.yaml'
                self.experiment_name = 'ys-default_ys2_ubuntu.yaml-2018_10_17_17_32_14'
                self.time = '2018_10_17_17_32_14'
                self.user = 'ys'
        self.stamp = STAMP()
        class TENSORBOARD:
            def __init__(self):
                self.enable = True
        self.tensorboard = TENSORBOARD()
        class TRACKER:
            def __init__(self):
                self.anchor = []
                self.context_amount = 0.5
                self.lr = 0.295
                self.penalty_k = 0.055
                self.ratios = [0.33, 0.5, 1, 2, 3]
                self.scales = [8]
                self.total_stride = 8
                self.window_influence = 0.42
                self.windowing = 'cosine'
        self.tracker = TRACKER()
        class TRAIN:
            def __init__(self):
                self.epochs = 10000
                self.log_interval = 10
                self.save_model_epoch_interval = 10
                self.valid_interval = 1
        self.train = TRAIN()
        class VISDOM:
            def __init__(self):
                self.enable = False
        self.visdom = VISDOM()
