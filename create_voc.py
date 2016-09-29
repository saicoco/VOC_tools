# -*- coding: utf-8 -*-
# author = sai

import xml.dom.minidom as xdm
import cv2, os
def to_xml(imagefile, root_dir, tempplate = 'template.xml', save_xml='./Annotations/', train=True):

    '''
    :param imagefile: image list
    :param root_dir: directory which image list and image locate
    :param tempplate: xml's format of VOC
    :param save_xml: dir where to save xml responding to image
    :param train: is or not train phase
    :return:
    '''
    if not os.path.exists('JEPGImages'):
        os.mkdir('JEPGImages')
    if not os.path.exists('Annotations'):
        os.mkdir('Annotations')
    if not os.path.exists('ImageSets'):
        os.mkdir('ImageSets')
    if not os.path.exists('ImageSets/Main'):
        os.mkdir('ImageSets/Main')

    if train:
        save_txt = './ImageSets/Main/trainval.txt'
    else:
        save_txt = './ImageSets/Main/test.txt'
    with open(imagefile, 'r') as f:
        for line in f.readlines():
            infos = line.split(' ')
            dirname, image = infos[0].split('\\')
            path = root_dir + '/' + dirname + '/' + image
            new_name = dirname + '_' + image
            im = cv2.imread(path)
            width, height, depth = im.shape
            xmin = infos[1]
            xmax = infos[2]
            ymin = infos[3]
            ymax = infos[4]

            '''parse xml'''
            dom = xdm.parse(tempplate)
            root = dom.documentElement

            filename_dom = root.getElementsByTagName('filename')
            filename_dom[0].firstChild.data = new_name

            width_dom = root.getElementsByTagName('width')
            width_dom[0].firstChild.data = width

            height_dom = root.getElementsByTagName('height')
            height_dom[0].firstChild.data = height

            depth_dom = root.getElementsByTagName('depth')
            depth_dom[0].firstChild.data = depth

            xmin_dom = root.getElementsByTagName('xmin')
            xmin_dom[0].firstChild.data = xmin

            xmax_dom = root.getElementsByTagName('xmax')
            xmax_dom[0].firstChild.data = xmax

            ymin_dom = root.getElementsByTagName('ymin')
            ymin_dom[0].firstChild.data = ymin

            ymax_dom = root.getElementsByTagName('ymax')
            ymax_dom[0].firstChild.data = ymax
            xml_prefix = new_name.split('.')[0]
            xml_filename = save_xml + xml_prefix + '.xml'
            with open(xml_filename, 'w') as f:
                     dom.writexml(f, encoding='utf-8')
            with open(save_txt, 'a+') as f:
                     f.write(xml_prefix)
                     f.write('\n')
            cv2.imwrite('JEPGImages/'+new_name, im)
if __name__ == '__main__':
    train_file = './train/trainImageList.txt'
    test_file = './train/testImageList.txt'
    print 'create train_dataset...'
    to_xml(train_file, root_dir='train', train=True)
    print 'create test_dataset...'
    to_xml(test_file, root_dir='train', train=False)
    print 'complete'
