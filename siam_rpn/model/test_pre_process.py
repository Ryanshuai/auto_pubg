import numpy as np
from config.siam_rpn.default_ys2_ubuntu import ARG
from data.data_utils import get_im_patch_by_pos_size
from .train_pre_process import generate_anchors


class Test_Pre:
    def __init__(self, arg: ARG):
        # ==============================================================================================================
        # z <=> exemplar
        # u <=> instance
        # cu, cz <=> crop u, crop z
        # tu, tz <=> target u, target z
        # mu, mz <=> model u, model z
        #
        # cx, cy, cpos <=> center x, center y, center pos
        # x, y <=> x_left_up, y_left_up
        # sz <=> size
        # ==============================================================================================================
        self.scales = arg.tracker.scales
        self.ratios = arg.tracker.ratios
        self.context_amount = arg.tracker.context_amount
        self.stride = arg.tracker.total_stride
        self.anchor_num = len(self.ratios) * len(self.scales)
        self.model_u_size = arg.model.u_size
        self.model_z_size = arg.model.z_size
        self.res_size = arg.model.res_size
        self.p_iou = 0.6
        self.n_iou = 0.3

        self.anchor_pos = []
        self.template_position = None
        self.ious = None
        self.cls_target = None
        self.reg_target = None
        self.anchors = self._generate_anchors()

    def _generate_anchors(self):
        ratios = self.ratios
        scales = self.scales
        stride = self.stride
        res_size = self.res_size

        anchors = generate_anchors(ratios, scales, stride, res_size)
        return anchors

    def get_z_from_im(self, im, target_center_pos, target_size):
        self.avg_color = np.mean(im, axis=(0, 1))

        wc_z = target_size[0] + self.context_amount * sum(target_size)
        hc_z = target_size[1] + self.context_amount * sum(target_size)
        crop_z_size = round(np.sqrt(wc_z * hc_z))

        model_z, _ = get_im_patch_by_pos_size(im, target_center_pos, crop_z_size, self.model_z_size, self.avg_color)
        return model_z

    def get_u_from_im(self, im, target_center_pos, target_size):
        self.target_u_center_pos = target_center_pos
        self.target_u_size = target_size
        wc_z = target_size[1] + self.context_amount * sum(target_size)
        hc_z = target_size[0] + self.context_amount * sum(target_size)
        s_z = np.sqrt(wc_z * hc_z)
        scale_z = self.model_z_size / s_z
        self.scale_z = scale_z
        d_search = (self.model_u_size - self.model_z_size) / 2
        pad = d_search / scale_z
        crop_u_size = round(s_z + 2 * pad)
        self.crop_u_size = crop_u_size

        model_u, resz_scale = get_im_patch_by_pos_size(im, target_center_pos, crop_u_size, self.model_u_size, self.avg_color)
        return model_u


# for test
def draw_anchors_with_annotation(img, pre):
    import cv2

    anchors = pre.anchors
    ious = pre.ious
    c_target = pre.cls_target
    r_target = pre.reg_target
    gt_ux, gt_uy, gt_uw, gt_uh = pre.model_u_xywh
    p_idx = pre.p_anchor_index
    # n_idx = pre.n_anchor_index_choice
    n_idx = pre.n_anchor_index

    img = cv2.rectangle(img, (gt_ux, gt_uy), (gt_ux + gt_uw, gt_uy + gt_uh), (255, 255, 255), thickness=3)
    print('gt:', gt_ux, gt_uy, gt_uw, gt_uh)

    for k, idx in enumerate(p_idx):
        an_x, an_y, an_w, an_h = anchors[idx]
        an_x, an_y, an_w, an_h = int(an_x), int(an_y), int(an_w), int(an_h)
        img = cv2.rectangle(img, (an_x, an_y), (an_x + an_w, an_y + an_h), (0, 255, 0), thickness=1)
        print('positive_anchor:', an_x, an_y, an_w, an_h)
        print('this anchor iou:', ious[idx])

        # test regression
        delta = r_target
        r_x = delta[k, 0] * anchors[k, 2] + anchors[k, 0]
        r_y = delta[k, 1] * anchors[k, 3] + anchors[k, 1]
        r_w = np.exp(delta[k, 2]) * anchors[k, 2]
        r_h = np.exp(delta[k, 3]) * anchors[k, 3]
        r_x, r_y, r_w, r_h = int(r_x), int(r_y), int(r_w), int(r_h)
        img = cv2.rectangle(img, (r_x, r_y), (r_x + r_w, r_y + r_h), (0, 255, 0), thickness=2)
        print('regression:', r_x, r_y, r_w, r_h)

    for i in n_idx:
        an_x, an_y, an_w, an_h = anchors[i]
        an_x, an_y, an_w, an_h = int(an_x), int(an_y), int(an_w), int(an_h)
        img = cv2.rectangle(img, (an_x, an_y), (an_x + an_w, an_y + an_h), (0, 0, 255), thickness=1)
        print('positive_anchor:', an_x, an_y, an_w, an_h)
        print('this anchor iou:', ious[i])

    return img


if __name__ == '__main__':
    import cv2
    from data.xml_2_dict import xml_2_xywh

    x, y, w, h = xml_2_xywh('000000.xml')
    im = cv2.imread('000000.JPEG')
    im_h, im_w, im_c = im.shape

    x_size = 255
    im = cv2.resize(im, (x_size, x_size))

    x, y, w, h = x*x_size//im_w, y*x_size//im_h, w*x_size//im_w, h*x_size//im_h

    im = cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 0), thickness=2)
    cv2.imshow('im', im)
    # cv2.waitKey(1)

    arg = ARG()
    pre = Pre(arg)
    pre.set_x_target_position(np.array([x, y, w, h]))
    pre.generate()
    rect_im = draw_anchors_with_annotation(im)

    cv2.imshow('im', rect_im)
    cv2.waitKey(0)

    print(9)

