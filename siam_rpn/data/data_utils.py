import numpy as np
import cv2
import torch


def get_im_patch_by_pos_size(im, center_pos, crop_sz, model_sz, avg_color):
    # get xmin, xmax ,ymin, ymax by center position and size
    sz = crop_sz  # size processed, nearly twice
    c = (crop_sz + 1) / 2
    context_xmin = int(round(center_pos[0] - c))  # floor(pos(2) - sz(2) / 2);
    context_xmax = int(context_xmin + sz - 1)
    context_ymin = int(round(center_pos[1] - c))  # floor(pos(1) - sz(1) / 2);
    context_ymax = int(context_ymin + sz - 1)

    # show_rect('before z_crop', im, center=center_pos, size=(crop_sz, crop_sz), color=(0, 0, 255), thickness=3)

    # if the nearly twice crop is out of image, compute the padding num
    im_sz = im.shape
    top_pad = int(max(0., -context_ymin))
    bottom_pad = int(max(0., context_ymax - im_sz[0] + 1))
    left_pad = int(max(0., -context_xmin))
    right_pad = int(max(0., context_xmax - im_sz[1] + 1))

    # covert to the crop in image
    context_xmin = context_xmin + left_pad
    context_xmax = context_xmax + left_pad
    context_ymin = context_ymin + top_pad
    context_ymax = context_ymax + top_pad

    # zzp: a more easy speed version
    r, c, k = im.shape
    # if has pad in four oriental:
    if any([top_pad, bottom_pad, left_pad, right_pad]):
        te_im = np.zeros((r + top_pad + bottom_pad, c + left_pad + right_pad, k), np.uint8)  # 0 is better than 1 initialization
        te_im[top_pad:top_pad + r, left_pad:left_pad + c, :] = im
        if top_pad:
            te_im[0:top_pad, left_pad:left_pad + c, :] = avg_color
        if bottom_pad:
            te_im[r + top_pad:, left_pad:left_pad + c, :] = avg_color
        if left_pad:
            te_im[:, 0:left_pad, :] = avg_color
        if right_pad:
            te_im[:, c + left_pad:, :] = avg_color
        im_patch_original = te_im[int(context_ymin):int(context_ymax + 1), int(context_xmin):int(context_xmax + 1), :]
    else:
        im_patch_original = im[int(context_ymin):int(context_ymax + 1), int(context_xmin):int(context_xmax + 1), :]
    assert im_patch_original.shape[0] == crop_sz and im_patch_original.shape[1] == crop_sz

    if not np.array_equal(model_sz, crop_sz):
        im_patch = cv2.resize(im_patch_original, (model_sz, model_sz))  # zzp: use cv to get a better speed
        model_divide_crop_scale = model_sz/crop_sz
    else:
        im_patch = im_patch_original
        model_divide_crop_scale = 1.

    # show_rect('after z_crop', im_patch)

    return im_patch, model_divide_crop_scale


def get_train_u_patch_cpos(im, center_pos, target_sz, crop_sz, model_sz, avg_color):
    # show_rect('before u_crop', im, center=center_pos, size=target_sz, color=(0,255,0), thickness=4)
    target_w, target_h = target_sz

    margin = crop_sz*0.2
    target_cx_min = target_w//2 + margin
    target_cx_max = crop_sz-target_w//2 - margin
    target_cy_min = target_h//2 + margin
    target_cy_max = crop_sz-target_h//2 - margin
    train_cx = np.random.randint(target_cx_min, target_cx_max)  # randint pick one in train_cx_range
    train_cy = np.random.randint(target_cy_min, target_cy_max)  # randint pick one in train_cy_range
    train_center_pos = np.array([train_cx, train_cy])

    # get xmin, xmax ,ymin, ymax by train cx cy
    context_xmin = int(round(center_pos[0] - train_cx))  # floor(pos(2) - sz(2) / 2);
    context_xmax = crop_sz+context_xmin-1
    context_ymin = int(round(center_pos[1] - train_cy))  # floor(pos(1) - sz(1) / 2);
    context_ymax = crop_sz+context_ymin-1

    # show_rect('before u_crop', im, center=center_pos, size=(crop_sz, crop_sz), color=(0, 0, 255), thickness=3)

    # if the nearly twice crop is out of image, compute the padding num
    im_sz = im.shape
    top_pad = int(max(0., -context_ymin))
    bottom_pad = int(max(0., context_ymax - im_sz[0] + 1))
    left_pad = int(max(0., -context_xmin))
    right_pad = int(max(0., context_xmax - im_sz[1] + 1))

    # covert to the crop in image
    context_xmin = context_xmin + left_pad
    context_xmax = context_xmax + left_pad
    context_ymin = context_ymin + top_pad
    context_ymax = context_ymax + top_pad

    # zzp: a more easy speed version
    r, c, k = im.shape
    # if has pad in four oriental:
    if any([top_pad, bottom_pad, left_pad, right_pad]):
        te_im = np.zeros((r + top_pad + bottom_pad, c + left_pad + right_pad, k), np.uint8)  # 0 is better than 1 initialization
        te_im[top_pad:top_pad + r, left_pad:left_pad + c, :] = im
        if top_pad:
            te_im[0:top_pad, left_pad:left_pad + c, :] = avg_color
        if bottom_pad:
            te_im[r + top_pad:, left_pad:left_pad + c, :] = avg_color
        if left_pad:
            te_im[:, 0:left_pad, :] = avg_color
        if right_pad:
            te_im[:, c + left_pad:, :] = avg_color
        im_patch_original = te_im[int(context_ymin):int(context_ymax + 1), int(context_xmin):int(context_xmax + 1), :]
    else:
        im_patch_original = im[int(context_ymin):int(context_ymax + 1), int(context_xmin):int(context_xmax + 1), :]
    assert im_patch_original.shape[0] == crop_sz and im_patch_original.shape[1] == crop_sz

    if not np.array_equal(model_sz, crop_sz):
        im_patch = cv2.resize(im_patch_original, (model_sz, model_sz))  # zzp: use cv to get a better speed
        model_divide_crop_scale = model_sz/crop_sz
    else:
        im_patch = im_patch_original
        model_divide_crop_scale = 1.

    train_size = target_sz*model_divide_crop_scale
    train_center_pos = train_center_pos*model_divide_crop_scale
    train_size = np.array([int(round(train_size[0])), int(round(train_size[1]))])
    train_center_pos = np.array([int(round(train_center_pos[0])), int(round(train_center_pos[1]))])
    # show_rect('after u_crop', im_patch, center=train_center_pos, size=train_size, color=(255,255,0), thickness=1)
    return im_patch, train_center_pos, train_size


def cxy_wh_to_rect(pos, sz):
    return np.array([pos[0]-sz[0]//2, pos[1]-sz[1]//2, sz[0], sz[1]])  # 0-index


def rect_to_cxy_wh(rect):
    return np.array([rect[0]+rect[2]//2, rect[1]+rect[3]//2]), np.array([rect[2], rect[3]])  # 0-index


def np_to_tensor(x, device):
    x = torch.from_numpy(x)
    x = x.float()
    x = x.to(device)
    if x.dim() == 3:
        x = torch.unsqueeze(x, 0)
    if x.shape[-1] == 3:
        x = x.permute((0, 3, 1, 2))
    return x


def to_numpy(tensor):
    if torch.is_tensor(tensor):
        return tensor.cpu().numpy()
    elif type(tensor).__module__ != 'numpy':
        raise ValueError("Cannot convert {} to numpy array"
                         .format(type(tensor)))
    return tensor


def im_to_numpy(img):
    img = to_numpy(img)
    if img.ndim == 3:
        img = np.transpose(img, (1, 2, 0))  # H*W*C
        return img
    if img.ndim == 4:
        img = np.transpose(img, (0, 2, 3, 1))  # BS*H*W*C
        return img


def im_to_np_255(img):
    img = im_to_numpy(img)
    img = img * 255
    return img.astype(dtype=np.uint8)


def nms(bboxes: np.ndarray, scores: np.ndarray, threshold):
    assert bboxes.shape[0] == scores.shape[0]

    # If no bounding boxes, return empty list
    if len(bboxes) == 0:
        return [], []

    # coordinates of bounding boxes
    start_x = bboxes[:, 0]
    start_y = bboxes[:, 1]
    end_x = bboxes[:, 2]
    end_y = bboxes[:, 3]

    # Picked bounding boxes
    picked_boxes = []
    picked_score = []

    # Compute areas of bounding boxes
    areas = (end_x - start_x + 1) * (end_y - start_y + 1)

    # Sort by confidence score of bounding boxes
    order = np.argsort(scores)

    # Iterate bounding boxes
    while order.size > 0:
        # The index of largest confidence score
        index = order[-1]

        # Pick the bounding box with largest confidence score
        picked_boxes.append(bboxes[index])
        picked_score.append(scores[index])
        a=start_x[index]
        b=order[:-1]
        c=start_x[order[:-1]]
        # Compute ordinates of intersection-over-union(IOU)
        x1 = np.maximum(start_x[index], start_x[order[:-1]])
        x2 = np.minimum(end_x[index], end_x[order[:-1]])
        y1 = np.maximum(start_y[index], start_y[order[:-1]])
        y2 = np.minimum(end_y[index], end_y[order[:-1]])

        # Compute areas of intersection-over-union
        w = np.maximum(0.0, x2 - x1 + 1)
        h = np.maximum(0.0, y2 - y1 + 1)
        intersection = w * h

        # Compute the ratio between intersection and union
        ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)

        left = np.where(ratio < threshold)
        order = order[left]

    return np.array(picked_boxes), np.array(picked_score)


def cord_2_regress(cord, anchor):
    assert cord.ndim == 1
    if anchor.ndim == 1:
        regress = np.zeros((4), dtype=np.float32)
        regress[0] = (cord[0] - anchor[0]) / anchor[2]
        regress[1] = (cord[1] - anchor[1]) / anchor[3]
        regress[2] = np.log(cord[2] / anchor[2])
        regress[3] = np.log(cord[3] / anchor[3])
        return regress

    if anchor.ndim == 2:
        num = anchor.shape[0]
        regress = np.zeros((num, 4), dtype=np.float32)
        for i in range(num):
            regress[i, 0] = (cord[0] - anchor[i, 0]) / anchor[i, 2]
            regress[i, 1] = (cord[1] - anchor[i, 1]) / anchor[i, 3]
            regress[i, 2] = np.log(cord[2] / anchor[i, 2])
            regress[i, 3] = np.log(cord[3] / anchor[i, 3])
        return regress


def regress_2_cord(regress, anchor):
    if regress.ndim == 1:
        delta = regress.copy()
        delta[0] = delta[0] * anchor[2] + anchor[0]
        delta[1] = delta[1] * anchor[3] + anchor[1]
        delta[2] = np.exp(regress[2]) * anchor[2]
        delta[3] = np.exp(regress[3]) * anchor[3]
        return delta

    if regress.ndim == 2:
        delta = regress.copy()
        delta[0, :] = delta[0, :] * anchor[:, 2] + anchor[:, 0]
        delta[1, :] = delta[1, :] * anchor[:, 3] + anchor[:, 1]
        delta[2, :] = np.exp(delta[2, :]) * anchor[:, 2]
        delta[3, :] = np.exp(delta[3, :]) * anchor[:, 3]
        return delta


def draw_rect(name, im, *args, **kwargs):

    if 'thickness' in kwargs:
        thickness = kwargs['thickness']
    else:
        thickness = 1

    if 'color' in kwargs:
        color = kwargs['color']
    else:
        color = (0, 0, 0)

    if 'center' in kwargs:
        center = kwargs['center']
        size = kwargs['size']
        x = center[0] - size[0] // 2
        y = center[1] - size[1] // 2
        w = size[0]
        h = size[1]
        x, y, w, h = int(x), int(y), int(w), int(h)
        im = cv2.rectangle(im, (x, y), (x+w, y+h), color, thickness=thickness)

    elif 'x' in kwargs:
        x = kwargs['x']
        y = kwargs['y']
        w = kwargs['w']
        h = kwargs['h']
        x, y, w, h = int(x), int(y), int(w), int(h)
        im = cv2.rectangle(im, (x, y), (x+w, y+h), color, thickness=thickness)

    is_show = True
    if 'not_show' in kwargs:
        is_show = not kwargs['not_show']
    if is_show:
        cv2.imshow(name, im)
        cv2.waitKey(0)

    return im

