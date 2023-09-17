from django.shortcuts import render
from .forms import myform
from .models import ImageModel
import cv2
import numpy as np
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from ultralytics import YOLO
import yaml

yaml_file_path = '/media/dheeraj/New_Volume/Waterloo-Work/HTN/coco.yaml'
with open(yaml_file_path, 'r') as file:
    yaml_data = yaml.safe_load(file)

# ROOT_DIR = 


def get_yolo_output(results, images):
    for result, image in zip(results, images):
        boxes = result.boxes  # Boxes object for bbox outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        img = cv2.imread(image)
        # print(" image widht is : {} and image height is : {}".format(img.shape[0], img.shape[1]))
        # exit(0)
        # cv2.imshow('output_frame', img)
        # cv2.waitKey(0)
        class_num = boxes.cls.numpy()
        class_name = yaml_data["names"][int(class_num)]
        boxes_arr = boxes.data.numpy()
        # print("boxes are :", boxes)
        # print(" boxes in numpy format are :", boxes_arr)

        top_left = (int(boxes_arr[0][0]), int(boxes_arr[0][1])) 
        top_border_center = (top_left[0] + int(boxes_arr[0][2]/2), top_left[1])
        # print(" top border center is : ", top_bord)
        # print(" top left is ", top_left)

        # bottom_right = boxes_arr[0][1] * img.shape[1] + boxes_arr[0][3] * img.shape[1]
        bottom_right = (int(boxes_arr[0][2]), int(boxes_arr[0][3]))
        # print(" bottom right is ", bottom_right)
        
        image_with_rectangle = cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)
        image_with_rectangle = cv2.putText(image_with_rectangle, class_name, top_border_center, cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)

        # cv2.imshow('output_frame', image_with_rectangle)
    return image_with_rectangle
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
model = YOLO('yolov8n.pt')  # pretrained YOLOv8n model


def home(request):
    images = []

    if request.method == 'POST':
        form = myform(request.POST, request.FILES)
        
        if form.is_valid():
            for image in request.FILES.getlist('Image'):
                images = [os.path.join("/media/dheeraj/New_Volume/Waterloo-Work/HTN/media/images/", image.name)]
                results = model(images)
                ImageModel.objects.create(Image=image)

    else:
        form = myform()
    
    # Fetch the latest uploaded image
    # image_model = ImageModel.objects.get(pk=)

    latest_image = ImageModel.objects.last()
    if latest_image:
        # print("type of latest image", type(latest_image))
        # Open the image using PIL
        image_pil = Image.open(latest_image.Image.path)
        # Convert PIL image to NumPy array
        image_np = np.array(image_pil)
        # Convert from BGR to RGB (if needed)
        if image_np.shape[-1] == 3:  # Check if the image has 3 channels (BGR)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        # Perform OpenCV operations on the NumPy array
        # top_left = (100, 100)
        # bottom_right = (200, 200)
        # color = (255, 0, 0)  # Red
        # thickness = 2
        image_with_rectangle = get_yolo_output(results, images)
        # Convert NumPy array back to PIL image
        image_with_rectangle_pil = Image.fromarray(image_with_rectangle)
        # Save the modified image to a BytesIO object
        output_buffer = BytesIO()
        image_with_rectangle_pil.save(output_buffer, format="PNG")
        # Create an InMemoryUploadedFile from the BytesIO object
        output_buffer.seek(0)
        modified_image = InMemoryUploadedFile(output_buffer, None, "new_image.png", "image/png", output_buffer.getbuffer().nbytes, None)
        # Create a new ImageModel instance with the modified image
        image_model = ImageModel(Image=modified_image)
        image_model.save()
    context = {'form': form, 'latest_image': image_model if latest_image else None}
    return render(request, 'uploadandisplay/home.html', context)