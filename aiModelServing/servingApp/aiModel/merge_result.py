import json
import os

def IoU(box1, box2):
    # box = (x1, y1, x2, y2)
    box1_area = abs((box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1))
    box2_area = abs((box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1))

    # obtain x1, y1, x2, y2 of the intersection
    x1 = max(box1[0], box2[0])
    y1 = min(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = max(box1[3], box2[3])

    # compute the width and height of the intersection
    w = max(0, x2 - x1 + 1)
    h = max(0, y1 - y2 + 1)
    inter = w * h
    iou = inter / (box1_area + box2_area - inter)
    return iou

def get_final_info(number_info, text_info):
    len_number = len(number_info)
    len_text = len(text_info)
    x = []
    for n in range(len_number):
        for t in range(len_text):
            box1 = number_info[n]['points'][3] + number_info[n]['points'][1]
            box2 = text_info[t]['points'][3] + text_info[t]['points'][1]
    
            iou_result = IoU(box1,box2)
            if iou_result == 0:
                #print(iou_result)
                x.append(number_info[n])
                break
    final = text_info + x
    return final

def make_final():
    image_list = os.listdir('servingApp/aiModel/image/')
    num_image = len(image_list)

    number = open("servingApp/aiModel/inference_results/number/system_results.txt", 'r')
    line_number = number.readlines()

    text = open("servingApp/aiModel/inference_results/system_results.txt", 'r')
    line_text = text.readlines()

    result = open("servingApp/aiModel/inference_results/final_results.txt", 'w')

    for i in range(num_image):
        number_line = line_number[i].split('\t')
        img_name_number = number_line[0]
        number_info = json.loads(number_line[1])

        text_line = line_text[i].split('\t')
        img_name_text = text_line[0]
        text_info = json.loads(text_line[1])

        final = get_final_info(number_info, text_info)
        final = json.dumps(final, ensure_ascii=False)
        final = img_name_text + '\t' +final + '\n'
        result.write(final)

    result.close()
    number.close()
    text.close()

if __name__ == "__main__":
    make_final()
    print('done')