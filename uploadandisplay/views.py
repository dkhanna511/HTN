# from django.shortcuts import render
# from .forms import myform
# from .models import ImageModel
# # import cv2
# # import numpy as np
# import os
# # TO RETRIEVE IMAGE NAME, USE image.name
# def home(request):
#     if request.method == 'POST':
#         form = myform(request.POST, request.FILES)
#         if form.is_valid():
#             for image in request.FILES.getlist('Image'):
#                 ImageModel.objects.create(Image=image)
#     else:
#         form = myform()
    
#     # Fetch the latest uploaded image
#     latest_image = ImageModel.objects.last()
    
#     context = {'form': form, 'latest_image': latest_image}

    
#     return render(request, 'home.html', context)
from django.shortcuts import render, redirect
from .forms import myform
from .models import ImageModel

def home(request):
    if request.method == 'POST':
        form = myform(request.POST, request.FILES)
        if form.is_valid():
            # Get the new image from the form
            new_image = form.cleaned_data['Image']

            # Fetch the latest uploaded image
            latest_image = ImageModel.objects.last()

            # If there's an existing image, delete it
            if latest_image:
                latest_image.Image.delete()

            # Create a new instance with the new image
            ImageModel.objects.create(Image=new_image)
    else:
        form = myform()
    
    # Fetch the latest uploaded image
    latest_image = ImageModel.objects.last()
    
    context = {'form': form, 'latest_image': latest_image}

    return render(request, 'home.html', context)

