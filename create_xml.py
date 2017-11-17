#! /usr/bin/python

import os, sys
import glob
from PIL import Image

src_img_dir = "/home/saicoco/code/car_ann/aug_images/"
src_txt_dir = "/home/saicoco/code/car_ann/aug_images/"

img_Lists = glob.glob(src_img_dir + '/*.jpg')

img_basenames = [] # e.g. 100.jpg
for item in img_Lists:
    img_basenames.append(os.path.basename(item))

img_names = [] # e.g. 100
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)

for img in img_names:
    im = Image.open((src_img_dir + '/' + img + '.jpg'))
    width, height = im.size

    # open the crospronding txt file
    gt = open(src_txt_dir + img + '.box').read().splitlines()

    # write in xml file
    filename = src_txt_dir + '/' + img + '.xml'
    if os.path.exists(filename):
        os.remove(filename)
        
    os.mknod(src_txt_dir + '/' + img + '.xml')
    xml_file = open((src_txt_dir + '/' + img + '.xml'), 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')

    # write the region of text on xml file
    for img_each_label in gt:
        spt = img_each_label.split('\t')
        # if eval(spt[0]) == 84:
        #     print img
        # print spt
        x2, y2 = eval(spt[1]) + eval(spt[3]), eval(spt[2]) + eval(spt[4])
        xml_file.write('    <object>\n')
        xml_file.write('        <name>' + str(spt[0]) + '</name>\n')
        xml_file.write('        <pose>Unspecified</pose>\n')
        xml_file.write('        <truncated>0</truncated>\n')
        xml_file.write('        <difficult>0</difficult>\n')
        xml_file.write('        <bndbox>\n')
        xml_file.write('            <xmin>' + str(spt[1]) + '</xmin>\n')
        xml_file.write('            <ymin>' + str(spt[2]) + '</ymin>\n')
        xml_file.write('            <xmax>' + str(x2) + '</xmax>\n')
        xml_file.write('            <ymax>' + str(y2) + '</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')

    xml_file.write('</annotation>')
