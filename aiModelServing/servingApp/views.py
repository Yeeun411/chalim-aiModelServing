from django.shortcuts import render

import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@csrf_exempt
def image_upload(request):
    if request.method == 'POST' and request.FILES['image']:
        # 이미지 파일 저장
        image_file = request.FILES['image']
        file_path = os.path.join('aiModelServing', 'servingApp', 'aiModel', 'image', image_file.name)
        file_name = default_storage.save(file_path, image_file)

        # run.sh 스크립트 실행
        script_path = os.path.join('servingApp', 'aiModel', 'run.sh')
        subprocess.run(['bash', script_path])

        # 결과 파일 읽기
        results_path = os.path.join('servingApp', 'aiModel', 'inference_results', 'final_results.txt')
        with open(results_path, 'r') as file:
            results = file.read()

        # 이미지 파일 삭제
        os.remove(file_path)

        # 결과 반환
        return JsonResponse({'result': results})

    return JsonResponse({'error': 'Invalid request'}, status=400)
