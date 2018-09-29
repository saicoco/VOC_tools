# VOC_tools

生成pascal voc 数据集
### 脚本说明
* process_img.py: 主要包含图像增强，用于构造数据  
* create_train_test_file.py: 创建list文件，用于得到VOC-series数据ImageSets/Main下txt文件  
* create_xml.py: 给出数据文件夹(包含box，jpg)，其中box中行内容为cls, x, y, w, h  

### Usage
```
./mask.sh original_dir target_dir
```
上述脚本中，original_dir为原始数据存放路径，包含xxx.jpg, xxx.txt文件，target_dir为暂存文件夹，
将会生成cls, inst, imgs三个文件夹，分别对应语义分割标签，实例分割标签，以及原始图片