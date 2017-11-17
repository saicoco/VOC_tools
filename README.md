# VOC_tools

* process_img.py: 主要包含图像增强，用于构造数据  
* create_train_test_file.py: 创建list文件，用于得到VOC-series数据ImageSets/Main下txt文件  
* create_xml.py: 给出数据文件夹(包含box，jpg)，其中box中行内容为cls, x, y, w, h  

完成上述脚本之后，将jpg, xml复制到VOC-series/JPEGImages|Annotations下面即可
