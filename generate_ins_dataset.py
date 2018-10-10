# coding=utf-8
import glob
import sys
import os
import shutil
import io
import cv2
import numpy as np

__author__ = 'gengjiajia'

"""
usage: python generate_ins_dataset.py data_dir out_dir

data_dir: input images and labels
out_dir: cls, inst, imgs, ImageSets/Main[train.txt|val.txt]
"""
data_dir = sys.argv[1]
out_dir = sys.argv[2]

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

    os.mkdir(os.path.join(out_dir, 'img'))
    os.mkdir(os.path.join(out_dir, 'cls'))
    os.mkdir(os.path.join(out_dir, 'inst'))

label_lists = glob.glob1(data_dir, '*.txt')
prefixs = map(lambda x: ".".join(x.split('.')[:-1]), label_lists)

for pref in prefixs:
    # copy img
    img_filename = os.path.join(data_dir, pref + '.jpg')
    out_cls_filename = os.path.join(out_dir, 'cls', pref + '.png')
    out_inst_filename = os.path.join(out_dir, 'inst', pref + '.png')
    try:
        img = cv2.imread(img_filename)
        img_shape = img.shape[:2]
    except:
        continue
    print img_shape
    h, w = img_shape[:2]
    cls_map = np.zeros(img_shape, dtype=np.uint8)
    inst_map = np.zeros(img_shape, dtype=np.uint8)
    print img_filename
    out_img_name = os.path.join(out_dir, 'img', pref + '.jpg')
    shutil.copy(img_filename, out_img_name)

    # generate cls map[bg:0, text:1]
    label_file = os.path.join(data_dir, pref + '.txt')
    with open(label_file, 'r') as f:
        all_lines = f.readlines()
    lines = []
    for line in all_lines:
        if len(line.strip('\n')) < 1:
            continue
        lines.append(line)
    all_boxes = []
    for i, line in enumerate(lines):
        # support rectangle box
        if len(line.split(',')) > 5:
            line_split = line.strip('\r\n').split(',')[:8]
        else:
            line_split = line.strip('\r\n').split(',')[:4]
            line_split = [line_split[0], line_split[1], line_split[2], line_split[1], line_split[2], line_split[3], line_split[0], line_split[3]]

        box = map(eval, line_split)
        box = np.array(box).reshape((-1, 2)).astype(np.float32)
        # rect_box
        l, t = np.amin(box, axis=0)
        r, b = np.amax(box, axis=0)
        str_box = ",".join(map(str, [l, t, r, b, 'text']))+'\n'
        all_boxes.append(str_box)

        rect_box = np.array([l, t, r, t, r, b, l, b]).reshape((-1, 2))
        # draw cls map
        cv2.fillPoly(cls_map, rect_box.astype(np.int32)[np.newaxis, :, :], 1)
        # draw inst map
        cv2.fillPoly(inst_map, box.astype(np.int32)[np.newaxis, :, :], 1)

    print 'cls_map_shape:', cls_map.shape
    cv2.imwrite(out_cls_filename, cls_map*255)
    cv2.imwrite(out_inst_filename, inst_map*255)
    tmp_box = out_img_name.split('.')
    tmp_box[-1] = 'txt'
    tmp_box = ".".join(tmp_box)
    with open(tmp_box, 'w') as f:
        f.writelines(all_boxes)
with open(os.path.join(out_dir, 'trainval.txt'), 'w') as f:
    prefixs = [pre + '\n' for pre in prefixs]
    f.writelines(prefixs)
