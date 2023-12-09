from flask import Flask, request, jsonify
import subprocess
import os
import time
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

ALLOWED_LANGUAGES = {"english", "japanese", "chinese"}

@app.route('/translate/<language>', methods=['POST'])
def run_model(language):

    # 언어 잘 전달됐는지 확인
    if language.lower() not in ALLOWED_LANGUAGES:
        return jsonify({'error': 'Invalid language'}), 400

    # Print the received language
    print("Received language:", language)


    # 이미지 이름 잘 전달됐는지 확인
    if 'imageName' not in request.form:
        return jsonify({'error': 'No imageName provided'}), 400
    image_name = request.form['imageName']
    # 이미지 파일 잘 전달됐는지 확인
    if 'imageFile' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    #이미지 파일 ./image 폴더에 저장
    image_file = request.files['imageFile']
    image_path = os.path.join('./image', image_name)
    try:
        image_file.save(image_path)
    except Exception as e:
        return jsonify({'error': f'Failed to save image: {str(e)}'}), 500

    # 모델 실행
    try:
        subprocess.run(['bash', 'run.sh'])
    except Exception as e:
        return jsonify({'error': f'Failed to run model: {str(e)}'}), 500

    # 모델 실행이 끝날 때까지 대기
    while not is_model_done():
        time.sleep(1)

    # 결과 읽어오기 및 처리
    results_path = './inference_results/final_results.txt'
    try:
        with open(results_path, 'r') as file:
            results = file.read()

            parts = results.split('\t', 1)
            image_name_result = parts[0]

            json_string = parts[1].strip()
            if not (json_string.startswith('[') or json_string.startswith('{')):
                return jsonify({'error': 'Invalid JSON format'}), 500

            translated_txt_result = json.loads(json_string)

            #json 파일에서 menuName, price 분리
            menuName = []
            price = []

            for item in translated_txt_result:
                if item['transcription'].isdigit():
                    price_item = {'priceValue': item['transcription'], 'points': item['points']}
                    price.append(price_item)
                else:
                    menuName.append(item)

            inference_results_path = './inference_results/'+image_name_result
            os.remove(inference_results_path)
            os.remove(image_path)
            # open(results_path, 'w').close()

            return {
                "imageName": image_name_result,
                "menuName": menuName,
                "price": price
            }

    except json.JSONDecodeError as e:
        return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to read results: {str(e)}'}), 500

# 모델 실행이 끝났는지 확인하는 함수: 텍스트 파일에 텍스트가 있는지 확인
def is_model_done():
    results_path = './inference_results/final_results.txt'
    return os.path.exists(results_path) and os.path.getsize(results_path) > 0

if __name__ == '__main__':
    app.run(debug=True)
