#! /usr/bin/python

import os, sys
import glob

trainval_dir = sys.argv[1]
test_dir = sys.argv[2]
dst_dir = sys.argv[3]
trainval_img_lists = glob.glob1(trainval_dir, '*.jpg')

if os.path.exists(dst_dir):
    os.mkdir(dst_dir)

dist_img_dir = os.path.join(dst_dir, "JPEGImages")
dist_anno_dir = os.path.join(dst_dir, "Annotations")

trainval_fd = open(os.path.join(dst_dir, "trainval.txt"), 'w')
test_fd = open(dst_dir,"test.txt", 'w')

import random
trainval_img_names = map(lambda x: x.split('.')[0] + '\n', trainval_img_lists)
random.shuffle(trainval_img_names)

length = len(trainval_img_names)
index = int(0.8 * length)
train_lst = trainval_img_names[:index]
test_lst = trainval_img_names[index:]

trainval_fd.writelines(train_lst)
test_fd.writelines(test_lst)

trainval_fd.close()
test_fd.close()
