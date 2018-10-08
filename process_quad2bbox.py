# coding=utf-8
import glob
import sys, os
import numpy as np

root_dir = sys.argv[1]
out_dir = sys.argv[2]
filelist = glob.glob1(root_dir, '*.txt')

for item in filelist:
    with open(item, 'r') as f:
        lines = f.readlines()
    for line in lines:
        box = np.array(map(lambda x:x.strip('\r\n').split(',')[:8]))
