python3 ./predict_system.py \
    --image_dir="./image" \
    --det_algorithm="DB++" \
    --det_model_dir="./model/detection" \
    --rec_model_dir="./model/recognition" \
    --rec_image_shape="3, 48, 320" \
    --rec_char_dict_path="./ppocr/utils/korean_dict.txt" \
    --use_gpu=False

python3 tools/infer/predict_system_num.py  \
    --det_model_dir='./det_nummodel_dir/' \
    --rec_model_dir='./rec_nummodel_dir/' \
    --image_dir="./image" \
    --rec_image_shape="3, 48, 320" \
    --draw_img_save_dir='./result/number/' \
    --rec_char_dict_path="./ppocr/utils/en_dict.txt" \
    --use_gpu=False
