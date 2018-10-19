class ARG:
    def __init__(self):
        self.device = 'cuda'
        self.device_ids = [0, 1, 2, 3]
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
                                self.num_workers = 8
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
                                self.root_path = '/simple_ssd/ys2/tracking_project/ILSVRC'
                        self.defaults = DEFAULTS()
                        class TRAIN:
                            def __init__(self):
                                self.annotation_path = 'Annotations/VID/train'
                                self.data_path = 'Data/VID/train'
                                self.root_path = '/simple_ssd/ys2/tracking_project/ILSVRC'
                        self.train = TRAIN()
                        class VALID:
                            def __init__(self):
                                self.annotation_path = 'Annotations/VID/train'
                                self.data_path = 'Data/VID/train'
                                self.root_path = '/simple_ssd/ys2/tracking_project/ILSVRC'
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
                self.lr = 5e-05
                self.weight_decay = 1e-05
        self.optim = OPTIM()
        class SAVE:
            def __init__(self):
                self.analyze = '/simple_ssd/ys2/tracking_project/siam_rpn/train_out/ys-default.yaml-2018_10_18_19_23_04/valid/coco_analyze'
                self.model = '/simple_ssd/ys2/tracking_project/siam_rpn/train_out/ys-default.yaml-2018_10_18_19_23_04/models'
                self.relative_analyze = 'valid/coco_analyze'
                self.relative_model = 'models'
                self.relative_tensorboard = 'tensorboard'
                self.relative_test = 'tst'
                self.relative_train = 'train'
                self.relative_valid = 'valid'
                self.root = '/simple_ssd/ys2/tracking_project/siam_rpn/train_out/ys-default.yaml-2018_10_18_19_23_04'
                self.root_ = '/simple_ssd/ys2/tracking_project/siam_rpn/train_out'
                self.tensorboard = '/simple_ssd/ys2/tracking_project/siam_rpn/train_out/ys-default.yaml-2018_10_18_19_23_04/tensorboard'
                self.test = '/simple_ssd/ys2/tracking_project/siam_rpn/train_out/ys-default.yaml-2018_10_18_19_23_04/tst'
                self.train = '/simple_ssd/ys2/tracking_project/siam_rpn/train_out/ys-default.yaml-2018_10_18_19_23_04/train'
                self.valid = '/simple_ssd/ys2/tracking_project/siam_rpn/train_out/ys-default.yaml-2018_10_18_19_23_04/valid'
        self.save = SAVE()
        class STAMP:
            def __init__(self):
                self.config_name = 'default.yaml'
                self.experiment_name = 'ys-default.yaml-2018_10_18_19_23_04'
                self.time = '2018_10_18_19_23_04'
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
