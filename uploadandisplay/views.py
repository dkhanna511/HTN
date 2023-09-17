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
    for image in request.FILES.getlist('Image'):
        wordE = "English:"
        wordE2 = image.name
        wordG = "German:"
        wordG2 = image.name
    context = {'form': form, 'latest_image': latest_image, 'wordE': wordE, 'wordE2': wordE2,  'wordG': wordG, 'wordG2': wordG2}

    return render(request, 'home.html', context)

