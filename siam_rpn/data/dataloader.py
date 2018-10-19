
from torch.utils.data import Dataset, DataLoader
from data.dataset import VID_Tracking_Dataset


class Tracking_TrainLoader(object):
    def __new__(cls, arg):
        train_data_set = VID_Tracking_Dataset(arg)
        pose_data_train_loader = DataLoader(dataset=train_data_set,
                                            batch_size=arg.data.dataloader.train.batch_size,
                                            shuffle=arg.data.dataloader.train.shuffle,
                                            num_workers=arg.data.dataloader.train.num_workers,
                                            pin_memory=True,
                                            drop_last=True)
        return pose_data_train_loader


class Tracking_ValidLoader(object):
    def __new__(cls, arg):
        valid_data_set = VID_Tracking_Dataset(arg)
        pose_data_valid_loader = DataLoader(dataset=valid_data_set,
                                            batch_size=arg.data.dataloader.valid.batch_size,
                                            shuffle=arg.data.dataloader.valid.shuffle,
                                            num_workers=arg.data.dataloader.valid.num_workers,
                                            pin_memory=True,
                                            drop_last=True)
        return pose_data_valid_loader
