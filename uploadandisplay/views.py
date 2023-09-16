from django.shortcuts import render
from .forms import myform
from .models import ImageModel
# import cv2
# import numpy as np
import os

def home(request):
    if request.method == 'POST':
        form = myform(request.POST, request.FILES)
        if form.is_valid():
            for image in request.FILES.getlist('Image'):
                ImageModel.objects.create(Image=image)
    else:
        form = myform()
    
    # Fetch the latest uploaded image
    latest_image = ImageModel.objects.last()
    
    context = {'form': form, 'latest_image': latest_image}
    
    return render(request, 'uploadandisplay/home.html', context)
