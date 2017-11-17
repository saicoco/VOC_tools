#! /usr/bin/python

import os, sys
import glob

trainval_dir = "/home/saicoco/code/car_ann/aug_images/"
test_dir = "/home/saicoco/code/car_ann/car_logo/aug_images/"

trainval_img_lists = glob.glob1(trainval_dir, '*.jpg')

# test_img_lists = glob.glob(test_dir + '/*.jpg')
# test_img_names = []
# for item in test_img_lists:
#     temp1, temp2 = os.path.splitext(os.path.basename(item))
#     test_img_names.append(temp1)

dist_img_dir = "cctv_logo/JPEGImages"
dist_anno_dir = "cctv_logo/Annotations"

trainval_fd = open("/home/saicoco/code/car_ann/cctv_logo/trainval.txt", 'w')
test_fd = open("/home/saicoco/code/car_ann/cctv_logo/test.txt", 'w')

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

# for item in test_img_names:
#     test_fd.write(dist_img_dir + '/' + str(item) + '.jpg' + ' ' + dist_anno_dir + '/' + str(item) + '.xml\n')
