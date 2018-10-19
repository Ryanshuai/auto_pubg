import os
import torch
import sys

from model.train_pre_process import *

sys.path.append(os.path.dirname(os.getcwd()))

from config.siam_rpn.default import ARG
from config.siam_rpn.default_ys2_ubuntu import ARG as ys_ARG
from data.dataloader import Tracking_TrainLoader, Tracking_ValidLoader
from Gear_tool.vis import Vis
from model.net import SiamRPN
from loss.rpn_loss import RPN_Loss
from Gear_tool.utils import prepare_save_dirs
from data.data_utils import *
import torch.nn.functional as F
from model.net_utils import load_pretrain


def train(arg, train_loader, model: SiamRPN, loss_func: RPN_Loss, optimizer, epoch, vis: Vis, anchors):
    for batch_idx, data in enumerate(train_loader):
        aidx = batch_idx + train_loader.__len__() * (epoch-1)

        z_batch, u_batch, cls_target_batch, cls_mask_batch, reg_target_batch, reg_mask_batch = data
        BS = z_batch.shape[0]

        z_batch = z_batch.to(arg.device)
        u_batch = u_batch.to(arg.device)
        cls_target_batch = cls_target_batch.to(arg.device)
        cls_mask_batch = cls_mask_batch.to(arg.device)
        reg_target_batch = reg_target_batch.to(arg.device)
        reg_mask_batch = reg_mask_batch.to(arg.device)

        optimizer.zero_grad()
        model.template(z_batch)
        cls_predict_m, reg_predict_m = model.forward(u_batch)

        batch_loss, batch_c_loss, batch_r_loss = 0., 0., 0.
        for bs_idx in range(BS):
            cls_predict_l = cls_predict_m[bs_idx].view(2, -1)
            cls_predict_l = cls_predict_l.permute(1, 0).contiguous()
            cls_target = cls_target_batch[bs_idx]
            cls_mask = cls_mask_batch[bs_idx]

            reg_predict_l = reg_predict_m[bs_idx].view(4, -1)
            reg_predict_l = reg_predict_l.permute(1, 0).contiguous()
            reg_target = reg_target_batch[bs_idx]
            reg_mask = reg_mask_batch[bs_idx]

            loss, c_loss, r_loss = loss_func.forward(cls_predict_l, cls_target, cls_mask, reg_predict_l, reg_target, reg_mask)
            batch_loss += loss
            batch_c_loss += c_loss
            batch_r_loss += r_loss
        batch_loss /= BS
        batch_c_loss /= BS
        batch_r_loss /= BS

        batch_loss.backward()
        # torch.nn.utils.clip_grad_norm(model.parameters(), 20)
        optimizer.step()

        # ====================================================================================================
        vis.line(win='train', name='loss', x=aidx, y=batch_loss.item())
        vis.line(win='train', name='c_loss', x=aidx, y=batch_c_loss.item())
        vis.line(win='train', name='r_loss', x=aidx, y=batch_r_loss.item())
        # print('-----------------------------')
        # print(loss.item(), c_loss.item(), r_loss.item())

        z_show = im_to_np_255(z_batch[0])
        u_show = im_to_np_255(u_batch[0])

        cls_predict_show = F.softmax(cls_predict_m[0].view(2, -1), dim=0).data[1, :]
        cls_predict_p = cls_predict_show.view(5, 17, 17).cpu().data.numpy()
        for i in range(5):
            cls_p = (cls_predict_p[i] * 255).astype(np.uint8)
            vis.img('feature', str(i)+'predict', cls_p, x=aidx)
        #     # cv2.imshow('predict'+str(i), cls_p)
        #     # cv2.waitKey(0)

        cls_target_show = cls_target_batch[0].view(5, 17, 17).cpu().data.numpy()
        for i in range(5):
            cls_t = (cls_target_show[i] * 255).astype(np.uint8)
            vis.img('feature', str(i)+'target', cls_t, x=aidx)
        #     # cv2.imshow('target'+str(i), cls_t)
        #     # cv2.waitKey(0)

        anchors_np = anchors.cpu().data.numpy()

        u_cls_target = u_show.copy()
        c_tar_np = cls_target_batch[0].cpu().data.numpy()
        for idx, c in enumerate(c_tar_np):
            if c > 0.7:
                x, y, w, h = anchors_np[idx]
                u_cls_target = draw_rect('', u_cls_target, x=x, y=y, w=w, h=h, color=(0, 255, 0), not_show=True)

        u_cls_predict = u_show.copy()
        c_pre = F.softmax(cls_predict_m[0].view(2, -1), dim=0).data[1, :]
        c_pre_np = c_pre.cpu().data.numpy()
        for idx, c in enumerate(c_pre_np):
            if c > 0.7:
                x, y, w, h = anchors_np[idx]
                u_cls_predict = draw_rect('', u_cls_predict, x=x, y=y, w=w, h=h, color=(0, 255, 255), not_show=True)

        u_reg_target = u_show.copy()
        reg_t = reg_target_batch[0] * reg_mask_batch[0].unsqueeze(1).type(torch.cuda.FloatTensor)
        reg_t = reg_t.permute(1, 0)
        reg_t = reg_t.cpu().data.numpy()
        cord = regress_2_cord(reg_t, anchors_np)
        for idx, c in enumerate(c_tar_np):
            if c > 0.7:
                x, y, w, h = cord[:, idx]
                u_reg_target = draw_rect('', u_reg_target, x=x, y=y, w=w, h=h, color=(0, 255, 0), not_show=True)

        u_reg_predict = u_show.copy()
        reg_pr = reg_predict_m[0].view(4, -1)
        reg_pr = reg_pr.cpu().data.numpy()
        cord = regress_2_cord(reg_pr, anchors_np)
        for idx, c in enumerate(c_pre_np):
            if c > 0.7:
                x, y, w, h = cord[:, idx]
                u_reg_predict = draw_rect('', u_reg_predict, x=x, y=y, w=w, h=h, color=(255, 255, 0), not_show=True)

        vis.img('1', 'z_show', z_show, x=aidx)
        vis.img('1', 'u_show', u_show, x=aidx)
        vis.img('cls', 'u_cls_target', u_cls_target, x=aidx)
        vis.img('cls', 'u_cls_predict', u_cls_predict, x=aidx)
        vis.img('reg', 'u_reg_target', u_reg_target, x=aidx)
        vis.img('reg', 'u_reg_predict', u_reg_predict, x=aidx)

        # cv2.imshow('z_show', z_show); cv2.waitKey(0)
        # cv2.imshow('u_show', u_show); cv2.waitKey(0)
        # cv2.imshow('u_cls_target', u_cls_target); cv2.waitKey(0)
        # cv2.imshow('u_cls_predict', u_cls_predict); cv2.waitKey(0)
        # cv2.imshow('u_reg_target', u_reg_target); cv2.waitKey(0)
        # cv2.imshow('u_reg_predict', u_reg_predict); cv2.waitKey(0)

# def valid(arg, valid_loader, model, epoch, vis):
#     for batch_idx, batch_data in enumerate(valid_loader):
#         z, x, cls_target, cls_mask, reg_target, reg_mask = batch_data
#         pass


def main():
    if os.path.exists('/home/'):
        arg = ys_ARG()
        print('ys_arg')
    else:
        arg = ARG()
        print('server_arg')

    vis = Vis(arg)

    prepare_save_dirs(arg)

    train_loader = Tracking_TrainLoader(arg)
    # valid_loader = Tracking_ValidLoader(arg)

    scales = arg.tracker.scales
    ratios = arg.tracker.ratios
    stride = arg.tracker.total_stride
    res_size = arg.model.res_size
    anchors = torch.from_numpy(generate_anchors_51717(ratios, scales, stride, res_size))

    model = SiamRPN().to(arg.device)
    pre_train_model_path = '../model/snapshot_only_classify_trained'
    # pre_train_model_path = '../tst/SiamRPNBIG.model'
    load_pretrain(model, pre_train_model_path)

    loss_func = RPN_Loss().to(arg.device)

    optimizer = torch.optim.SGD(model.training_pram(), lr=arg.optim.lr, weight_decay=arg.optim.weight_decay)

    for epoch in range(1, arg.train.epochs + 1):
        train(arg, train_loader, model, loss_func, optimizer, epoch, vis, anchors)

        # if epoch % arg.train.valid_interval == 0:
        #     valid(arg, valid_loader, model, epoch, vis)

        if epoch % arg.train.save_model_epoch_interval == 0:
            torch.save(model.state_dict(), os.path.join(arg.save.model, 'snapshot_epoch{}_model'.format(epoch)))


if __name__ == '__main__':
    main()
