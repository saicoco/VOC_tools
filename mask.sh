root_dir=$1
tmp_dir=$2
python generate_ins_dataset.py $root_dir $tmp_dir
python create_xml.py $tmp_dir/img/ $tmp_dir/img/

mkdir VOC2012
cd VOC2012/
mkdir Annotations
mkdir JPEGImages
mkdir segmentation_labels
mkdir -p ImageSets/Main
cd ..
mv $tmp_dir/img/*.jpg VOC2012/JPEGImages/
mv $tmp_dir/img/*.xml VOC2012/Annotations/
mv $tmp_dir/trainval.txt VOC2012/ImageSets/Main
mv $tmp_dir/cls/*.png VOC2012/segmentation_labels
rm -rf $tmp_dir

python create_train_test_file.py VOC2012/JPEGImages/ VOC2012/ImageSets/Main/