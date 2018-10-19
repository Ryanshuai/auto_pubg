import cv2
import numpy as np
from config.siam_rpn.default_ys2_ubuntu import ARG
from data.data_utils import *


class Train_Pre:
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
        self.stride = arg.tracker.total_stride
        self.res_size = arg.model.res_size
        self.context_amount = arg.tracker.context_amount
        self.anchor_num = len(self.ratios) * len(self.scales)
        self.model_u_size = arg.model.u_size
        self.model_z_size = arg.model.z_size
        self.p_iou = 0.6
        self.n_iou = 0.3

        self.anchor_pos = []
        self.template_position = None
        self.ious = None
        self.cls_target = None
        self.reg_target = None
        self.anchors = self._generate_anchors()
        # self.anchors += np.array([128 ,128, 0, 0])

    def _generate_anchors(self):
        ratios = self.ratios
        scales = self.scales
        stride = self.stride
        res_size = self.res_size

        anchors = generate_anchors_51717(ratios, scales, stride, res_size)
        return anchors

    def get_z_from_im(self, im, target_center_pos, target_size):

        # show_rect('z_before crop', im, center=target_center_pos, size=target_size)

        self.avg_color = np.mean(im, axis=(0, 1))

        wc_z = target_size[0] + self.context_amount * sum(target_size)
        hc_z = target_size[1] + self.context_amount * sum(target_size)
        crop_z_size = round(np.sqrt(wc_z * hc_z))

        model_z, _ = get_im_patch_by_pos_size(im, target_center_pos, crop_z_size, self.model_z_size, self.avg_color)
        return model_z

    def get_u_from_im(self, im, target_center_pos, target_size):
        wc_z = target_size[1] + self.context_amount * sum(target_size)
        hc_z = target_size[0] + self.context_amount * sum(target_size)
        s_z = np.sqrt(wc_z * hc_z)
        scale_z = self.model_z_size / s_z
        self.scale_z = scale_z
        d_search = (self.model_u_size - self.model_z_size) / 2
        pad = d_search / scale_z
        crop_u_size = round(s_z + 2 * pad)

        model_u, train_center_pos, train_size = get_train_u_patch_cpos(im, target_center_pos, target_size, crop_u_size,
                                                           self.model_u_size, self.avg_color)
        self.train_u_rect = cxy_wh_to_rect(train_center_pos, train_size)
        return model_u

    def _mat_IOU(self):
        x0, y0, w0, h0 = self.train_u_rect
        mat = self.anchors
        x1, y1, w1, h1 = mat[:, 0], mat[:, 1], mat[:, 2], mat[:, 3]

        startx = np.minimum(x1, x0)
        endx = np.maximum(x1+w1, x0+w0)
        width = w1+w0-(endx-startx)

        starty = np.minimum(y1, y0)
        endy = np.maximum(y1+h1, y0+h0)
        height = h1+h0-(endy-starty)

        width = np.maximum(width, 0)
        height = np.maximum(height, 0)

        Area = width * height
        Area0 = w0 * h0
        Area1 = w1 * h1
        ious = Area * 1. / (Area0 + Area1 - Area)

        self.ious = ious

    def _get_pos_and_neg_anchor_pos(self):
        ious = self.ious
        p_anchor_pos = np.where(ious >= self.p_iou, 1, 0)
        n_anchor_pos = np.where(ious <= self.n_iou, 1, 0)

        if np.max(ious) < self.p_iou:
            # print('only one positive iou')
            max_index = int(np.argmax(ious))
            p_anchor_pos[max_index] = 1
            n_anchor_pos[max_index] = 0

        self.p_index = np.array(np.where(p_anchor_pos == 1)[0])
        self.n_index = np.array(np.where(n_anchor_pos == 1)[0])
        n_anchor_num = len(self.p_index) * 3
        self.n_index_choice = np.array(np.random.choice(self.n_index, size=n_anchor_num))

        n_anchor_mask = np.zeros_like(n_anchor_pos)
        n_anchor_mask[self.n_index_choice] = 1
        # n_anchor_mask[self.n_index] = 1  # only for test negative position

        n_anchor_mask = n_anchor_mask
        p_anchor_mask = p_anchor_pos

        self.cls_target = p_anchor_pos
        self.reg_target = cord_2_regress(self.train_u_rect, self.anchors)

        self.cls_mask = (p_anchor_mask + n_anchor_mask)
        assert max(self.cls_mask) < 1.1

        self.reg_mask = p_anchor_mask

    def return_ct_cm_rt_rm(self):
        self._mat_IOU()
        self._get_pos_and_neg_anchor_pos()
        return self.cls_target, self.cls_mask, self.reg_target, self.reg_mask, self.p_index, self.n_index_choice


# center 5,17,17
def generate_anchors_51717(ratios, scales, total_stride, score_size):
    anchor_num = len(ratios) * len(scales)
    anchors = np.zeros((anchor_num, 4),  dtype=np.float32)
    size = total_stride * total_stride
    count = 0
    for ratio in ratios:
        ws = int(np.sqrt(size / ratio))
        hs = int(ws * ratio)
        for scale in scales:
            wws = ws * scale
            hhs = hs * scale

            center = 62
            anchors[count, 0] = center-wws//2      # x
            anchors[count, 1] = center-hhs//2      # y
            anchors[count, 2] = wws                # w
            anchors[count, 3] = hhs                # h
            count += 1

    anchors = np.tile(anchors, score_size * score_size).reshape((-1, 4))
    # ori = - (score_size / 2) * total_stride
    ori = 0
    xx, yy = np.meshgrid([ori + total_stride * dx for dx in range(score_size)],
                         [ori + total_stride * dy for dy in range(score_size)])
    xx, yy = np.tile(xx.flatten(), (anchor_num, 1)).flatten(), \
             np.tile(yy.flatten(), (anchor_num, 1)).flatten()
    anchors[:, 0] += xx.astype(np.int)
    anchors[:, 1] += yy.astype(np.int)
    return anchors


# center 17,17,5
def generate_anchors_17175(ratios, scales, stride, res_size):
    anchor_num = len(ratios) * len(scales)
    anchors = np.zeros((anchor_num, 4),  dtype=np.float32)
    size = stride * stride
    count = 0
    for ratio in ratios:
        ws = int(np.sqrt(size // ratio))
        hs = int(ws * ratio)
        for scale in scales:
            wws = ws * scale
            hhs = hs * scale
            center = 62

            anchors[count, 0] = center-wws//2      # x
            anchors[count, 1] = center-hhs//2      # y
            anchors[count, 2] = wws                # w
            anchors[count, 3] = hhs                # h
            count += 1

    anchors = np.repeat(anchors, res_size * res_size).reshape((-1, 4))  # shape(5, 4)->shape(2205, 4)

    yy = np.array([stride * dy for dy in range(res_size)])
    xx = np.array([stride * dx for dx in range(res_size)])

    yy = np.repeat(yy, anchor_num)
    xx = np.repeat(xx, anchor_num)

    yy = np.repeat(yy, res_size)
    xx = np.tile(xx, res_size)

    anchors[:, 0] += yy.astype(np.int)
    anchors[:, 1] += xx.astype(np.int)

    # anchors = anchors.reshape([self.f_size_h, self.f_size_w, self.anchor_num, -1])

    return anchors


# author's
def generate_anchors(ratios, scales, total_stride, score_size):
    anchor_num = len(ratios) * len(scales)
    anchor = np.zeros((anchor_num, 4),  dtype=np.float32)
    size = total_stride * total_stride
    count = 0
    for ratio in ratios:
        ws = int(np.sqrt(size / ratio))
        hs = int(ws * ratio)
        for scale in scales:
            wws = ws * scale
            hhs = hs * scale
            anchor[count, 0] = 0
            anchor[count, 1] = 0
            anchor[count, 2] = wws
            anchor[count, 3] = hhs
            count += 1

    anchor = np.tile(anchor, score_size * score_size).reshape((-1, 4))
    ori = - (score_size / 2) * total_stride
    xx, yy = np.meshgrid([ori + total_stride * dx for dx in range(score_size)],
                         [ori + total_stride * dy for dy in range(score_size)])
    xx, yy = np.tile(xx.flatten(), (anchor_num, 1)).flatten(), \
             np.tile(yy.flatten(), (anchor_num, 1)).flatten()
    anchor[:, 0], anchor[:, 1] = xx.astype(np.float32), yy.astype(np.float32)
    return anchor


# for test
def draw_anchors_with_annotation(img, pre: Train_Pre):
    anchors = pre.anchors
    ious = pre.ious
    gt_ux, gt_uy, gt_uw, gt_uh = pre.train_u_rect
    p_idx = pre.p_index
    n_idx = pre.n_index_choice
    # n_idx = pre.n_anchor_index
    p_regresses = pre.reg_target[p_idx, :]
    p_anchors = anchors[p_idx, :]

    img = cv2.rectangle(img, (gt_ux, gt_uy), (gt_ux + gt_uw, gt_uy + gt_uh), (255, 255, 255), thickness=3)
    print('gt:', gt_ux, gt_uy, gt_uw, gt_uh)

    for k, (idx, anchor, regress) in enumerate(zip(p_idx, p_anchors, p_regresses)):
        an_x, an_y, an_w, an_h = anchor
        an_x, an_y, an_w, an_h = int(an_x), int(an_y), int(an_w), int(an_h)
        img = cv2.rectangle(img, (an_x, an_y), (an_x + an_w, an_y + an_h), (0, 255, 0), thickness=1)
        print('positive_anchor:', an_x, an_y, an_w, an_h)
        print('this anchor iou:', ious[idx])

        # test regression
        r_x, r_y, r_w, r_h = regress_2_cord(regress, anchor)
        r_x, r_y, r_w, r_h = int(r_x), int(r_y), int(r_w), int(r_h)
        img = cv2.rectangle(img, (r_x, r_y), (r_x + r_w, r_y + r_h), (255, 255, 0), thickness=2)
        print('regression:', r_x, r_y, r_w, r_h)

    # for i in n_idx:
    #     an_x, an_y, an_w, an_h = anchors[i]
    #     an_x, an_y, an_w, an_h = int(an_x), int(an_y), int(an_w), int(an_h)
    #     img = cv2.rectangle(img, (an_x, an_y), (an_x + an_w, an_y + an_h), (0, 0, 255), thickness=1)
    #     print('positive_anchor:', an_x, an_y, an_w, an_h)
    #     print('this anchor iou:', ious[i])

    return img


# for test
def draw_anchors(img, pre):
    anchors = pre.anchors

    for anchor in anchors:
        an_x, an_y, an_w, an_h = anchor
        an_x, an_y, an_w, an_h = int(an_x), int(an_y), int(an_w), int(an_h)
        img = cv2.rectangle(img, (an_x, an_y), (an_x + an_w, an_y + an_h), (0, 255, 0), thickness=1)

        cv2.imshow('pre.anchors: ', img)
        cv2.waitKey()

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
    pre = Train_Pre(arg)



    print(9)

