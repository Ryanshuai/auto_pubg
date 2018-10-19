import torch.nn as nn
import torch.nn.functional as F
import torch.utils.model_zoo as model_zoo

model_urls = {'alexnet': 'https://download.pytorch.org/models/alexnet-owt-4df8aa71.pth'}


class SiamRPN(nn.Module):
    def __init__(self, feat_in=512, feature_out=512, anchor_num=5):
        super().__init__()
        self.anchor_num = anchor_num
        self.feature_out = feature_out
        self.featureExtract = nn.Sequential(
            nn.Conv2d(3, 192, 11, stride=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            nn.Conv2d(192, 512, 5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),
            nn.Conv2d(512, 768, 3),
            nn.ReLU(inplace=True),
            nn.Conv2d(768, 768, 3),
            nn.ReLU(inplace=True),
            nn.Conv2d(768, 512, 3),
        )

        # self.featureExtract = nn.Sequential(
        #     nn.Conv2d(3, 192, 11, stride=2),
        #     nn.BatchNorm2d(192),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(3, stride=2),
        #     nn.Conv2d(192, 512, 5),
        #     nn.BatchNorm2d(512),
        #     nn.ReLU(inplace=True),
        #     nn.MaxPool2d(3, stride=2),
        #     nn.Conv2d(512, 768, 3),
        #     nn.BatchNorm2d(768),
        #     nn.ReLU(inplace=True),
        #     nn.Conv2d(768, 768, 3),
        #     nn.BatchNorm2d(768),
        #     nn.ReLU(inplace=True),
        #     nn.Conv2d(768, 512, 3),
        #     nn.BatchNorm2d(512),
        # )

        self.conv_r1 = nn.Conv2d(feat_in, feature_out*4*anchor_num, kernel_size=3)
        self.conv_r2 = nn.Conv2d(feat_in, feature_out, kernel_size=3)
        self.conv_cls1 = nn.Conv2d(feat_in, feature_out*2*anchor_num, kernel_size=3)
        self.conv_cls2 = nn.Conv2d(feat_in, feature_out, kernel_size=3)
        self.regress_adjust = nn.Conv2d(4*anchor_num, 4*anchor_num, kernel_size=1)

        self.r1_kernel = []
        self.cls1_kernel = []
        self.training_params = []
        self._find_training_params()
        # self._set_feature_net_params()

    def _find_training_params(self):
        self.training_params += list(self.featureExtract[6].parameters())
        self.training_params += list(self.featureExtract[8].parameters())
        self.training_params += list(self.featureExtract[10].parameters())
        self.training_params += list(self.conv_r1.parameters())
        self.training_params += list(self.conv_r2.parameters())
        self.training_params += list(self.conv_cls1.parameters())
        self.training_params += list(self.conv_cls2.parameters())
        self.training_params += list(self.regress_adjust.parameters())

    def _set_feature_net_params(self):
        pretrained_dict = model_zoo.load_url(model_urls['alexnet'])
        model_dict = self.state_dict()
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
        model_dict.update(pretrained_dict)
        self.load_state_dict(model_dict)

    def template(self, z):
        z_f = self.featureExtract.forward(z)
        r1_kernel_raw = self.conv_r1(z_f)
        cls1_kernel_raw = self.conv_cls1(z_f)
        kernel_size = r1_kernel_raw.data.size()[-1]
        self.r1_kernel = r1_kernel_raw.view(self.anchor_num * 4, self.feature_out, kernel_size, kernel_size)
        self.cls1_kernel = cls1_kernel_raw.view(self.anchor_num * 2, self.feature_out, kernel_size, kernel_size)

    def forward(self, x):
        x_f = self.featureExtract.forward(x)
        cls_predict = F.conv2d(self.conv_cls2(x_f), self.cls1_kernel)
        reg_predict = self.regress_adjust(F.conv2d(self.conv_r2(x_f), self.r1_kernel))
        return cls_predict, reg_predict

    def training_pram(self):
        return self.training_params
