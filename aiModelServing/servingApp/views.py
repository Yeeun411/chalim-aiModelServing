from django.shortcuts import render

import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@csrf_exempt
def image_upload(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        file_path = os.path.join('aiModelServing', 'servingApp', 'aiModel', 'image', image_file.name)
        file_name = default_storage.save(file_path, image_file)

        subprocess.run(['bash', 'run.sh'])

        results_path = os.path.join('aiModelServing', 'servingApp', 'aiModel', 'inference_results', 'final_results.txt')
        with open(results_path, 'r') as file:
            results = file.read()

        return JsonResponse({'result': results})

    return JsonResponse({'error': 'Invalid request'}, status=400)
