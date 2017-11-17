# coding=utf-8
import glob
import numpy as np
import cv2

img_root = "images/"
line_item = ["logo\t"]
images_lst = glob.glob1(img_root, "*.jpg")
ori_x, ori_y, ori_w, ori_h = 1013, 524, 150, 143
default_line = ["logo\t1013\t524\t150\t143\n"]
num_w = 1280//ori_w
num_h = 720//ori_h

def random_loc(num_h=num_h, num_w=num_w):
    w_ind = np.random.randint(2, num_w-2)
    h_ind = np.random.randint(2, num_h-2)

    random_x = ori_w * w_ind
    random_y = ori_h * h_ind

    return [random_x, random_y]

def random_scale(img):
    prob = np.random.uniform(-1, 1)
    new_size = None
    if -0.5 < prob <= 0:
        new_size = [ori_w*2, ori_h*2]
    elif 0 < prob <= 0.5:
        new_size = [ori_w//2, ori_h//2]
    elif 0.5 < prob < 0.7:
        new_size = [ori_w//1, ori_h//1]
    elif 0.7 < prob:
        new_size = [ori_w*3//2, ori_h*3//2]
    elif -0.5 > prob> -0.3:
        new_size = [ori_w*3, ori_h*3]
    else:
        new_size = [ori_w//3, ori_h//3]
    return cv2.resize(img, dsize=tuple(new_size), interpolation=cv2.INTER_CUBIC), new_size 

def random_flip(img):
    prob = np.random.uniform(-1, 1)
    if -0.5 < prob <= 0:
        return cv2.flip(img, 0)
    elif 0 < prob <= 0.5:
        return cv2.flip(img, 1)
    elif 0.5 < prob:
        return cv2.flip(img, -1)
    else:
        return img

def rotate_img(img):
    prob = np.random.uniform(-1, 1)
    h,w = img.shape[:2]
    center = (w / 2,h / 2)
    if -0.5 < prob <= 0:
        M = cv2.getRotationMatrix2D(center,90,1)#旋转缩放矩阵：(旋转中心，旋转角度，缩放因子)
        
    elif 0 < prob <= 0.5:
        M = cv2.getRotationMatrix2D(center,180,1)
    elif 0.5 < prob:
        M = cv2.getRotationMatrix2D(center,270,1)
    else:
        M = cv2.getRotationMatrix2D(center,360,1)

    return cv2.warpAffine(img,M,(w,h))

def process_logo_image(logo_img, num_h=num_h, num_w=num_w):
    x, y = random_loc(num_h, num_w)
    prob = np.random.uniform(-1, 1)
    if prob>0:
        logo_img = random_flip(logo_img)
    else:
        logo_img = rotate_img(logo_img)
    new_img, new_size = random_scale(logo_img)
    return new_img, [x, y] + new_size

def main(data_root="aug_images/"):
    for i, item in enumerate(images_lst):
        print item
        img = cv2.imread(img_root + item)
        with open(data_root + item.split('.')[0] + '.box', 'w') as f:
            f.writelines(default_line)
        cv2.imwrite(data_root + item, img)

        logo_img = img[ori_y:ori_y+ori_h, ori_x:ori_w+ori_x, :]
        for j in xrange(10):
            tmp = img.copy()
            new_logo, loc = process_logo_image(logo_img)
            x, y, w, h = loc
            tmp[y:y+h, x:x+w, :] = new_logo
            new_line = ['logo\t'] + map(lambda x: str(x) + '\t', [x, y, w]) + [str(h) + '\n']
            with open(data_root + item.split('.')[0] + "_"+ str(j) + '.box', 'w') as f:
                f.writelines(["".join(new_line)] + default_line)
            cv2.imwrite(data_root + item.split('.')[0] + "_"+ str(j) + '.jpg', tmp)
            del tmp
            # cv2.rectangle(img, (loc[0], loc[1]), (loc[0]+loc[2], loc[1]+loc[3]), (0, 225, 0), 5)
            # cv2.imwrite("demo.jpg", img)
def process_flicker8k(data_root="aug_images/"):
    img_root = "flicker8k/"
    line_item = ["logo\t"]
    images_lst = glob.glob1(img_root, "*.jpg")
    ori_x, ori_y, ori_w, ori_h = 1013, 524, 150, 143
    default_line = ["logo\t1013\t524\t150\t143\n"]
    # num_w = 1280//ori_w
    # num_h = 720//ori_h
    img = cv2.imread('logo.jpg')
    logo_img = img[ori_y:ori_y+ori_h, ori_x:ori_w+ori_x, :]
    for i, item in enumerate(images_lst):
        print item
        img = cv2.imread(img_root + item)
        # with open(data_root + item.split('.')[0] + '.box', 'w') as f:
        #     f.writelines(default_line)
        # tmp_ = img.copy()
        # tmp_[ori_y:ori_y+ori_h, ori_x:ori_x+ori_w, :] = logo_img
        # cv2.imwrite(data_root + item, img)

        
        for j in xrange(10):
            tmp = img.copy()
            h, w = img.shape[:2]
            num_w = w//ori_w
            num_h = h//ori_h
            new_logo, loc = process_logo_image(logo_img, num_h, num_w)
            x, y, w, h = loc
            # print new_logo.shape, loc
            
            new_logo[new_logo>250] = 0
            # print mask[0].shape, mask[1].shape, new_logo.shape
            for xt in xrange(w):
                for yt in xrange(h):
                    tmp[y:y+yt, x:x+xt, :] = tmp[y:y+yt, x:x+xt, :] if not new_logo[yt, xt, :].all() else new_logo[yt, xt, :]
            # tmp[y:y+h, x:x+w, :] = new_logo
            new_line = ['logo\t'] + map(lambda x: str(x) + '\t', [x, y, w]) + [str(h) + '\n']
            with open(data_root + item.split('.')[0] + "_"+ str(j) + '.box', 'w') as f:
                f.writelines(["".join(new_line)] + default_line)
            cv2.imwrite(data_root + item.split('.')[0] + "_"+ str(j) + '.jpg', tmp)
            del tmp
if __name__=="__main__":
    main()
    
        
    
