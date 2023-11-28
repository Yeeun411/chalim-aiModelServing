python3 ./predict_system.py \
    --image_dir="./image" \
    --det_algorithm="DB++" \
    --det_model_dir="./model/detection" \
    --rec_model_dir="./model/recognition" \
    --rec_image_shape="3, 48, 320" \
    --rec_char_dict_path="./ppocr/utils/korean_dict.txt" \
    --use_gpu=False