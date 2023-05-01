import os
import subprocess
import sys

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

def predict_caption(request):
    if request.method == 'POST':
        # get the uploaded image file
        img_file = request.FILES['image']

        # save the image to a temporary file
        # save the image to a temporary file
        temp_img_path = os.path.join(settings.BASE_DIR, 'F:\Saafi\captioning\captionGenerator\static', 'temp_img.png')

        with open(temp_img_path, 'wb+') as f:
            for chunk in img_file.chunks():
                f.write(chunk)

        # run the predict.py script with the temporary image file as an argument
        predict_script_path = os.path.join(settings.BASE_DIR, 'clip-gpt-captioning', 'src', 'predict.py')
        cmd = [sys.executable, predict_script_path, '-I', temp_img_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)

        # extract the generated caption from the script's output
        caption = result.stdout.decode().strip()

        # return the generated caption to the user
        return render(request,'result.html',{'caption': caption})

    # render the image upload form for GET requests
    return render(request, 'index.html')
