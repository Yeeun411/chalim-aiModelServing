python3 servingApp/aiModel/predict_system.py \
    --image_dir="servingApp/aiModel//image" \
    --det_algorithm="DB++" \
    --det_model_dir="servingApp/aiModel//model/detection" \
    --rec_model_dir="servingApp/aiModel//model/recognition" \
    --rec_image_shape="3, 48, 320" \
    --rec_char_dict_path="servingApp/aiModel//ppocr/utils/korean_dict.txt" \
    --use_gpu=False

python3 servingApp/aiModel//predict_system_num.py  \
    --det_model_dir='servingApp/aiModel//model/det_nummodel_dir/' \
    --rec_model_dir='servingApp/aiModel//model/rec_nummodel_dir/' \
    --image_dir="servingApp/aiModel//image" \
    --rec_image_shape="3, 48, 320" \
    --draw_img_save_dir='servingApp/aiModel//inference_results/number/' \
    --rec_char_dict_path="servingApp/aiModel//ppocr/utils/en_dict.txt" \
    --use_gpu=False

python3 servingApp/aiModel//merge_result.py
