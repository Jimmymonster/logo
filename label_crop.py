import os
import cv2

data_path = 'cropdata'
images_path  = os.path.join(data_path, 'images')
labels_path  = os.path.join(data_path, 'labels')
output_path  = 'cropped_images'

os.makedirs(output_path, exist_ok=True)

def crop_image(image, labels):
    h, w, _ = image.shape
    cropped_images = []
    
    for label in labels:
        cls, x_center, y_center, bbox_width, bbox_height = label
        x_center, y_center, bbox_width, bbox_height = float(x_center), float(y_center), float(bbox_width), float(bbox_height)
        x_center *= w
        y_center *= h
        bbox_width *= w
        bbox_height *= h
        x1 = int(x_center - bbox_width / 2)
        y1 = int(y_center - bbox_height / 2)
        x2 = int(x_center + bbox_width / 2)
        y2 = int(y_center + bbox_height / 2)
        cropped_image = image[y1:y2, x1:x2]
    cropped_images.append((cls, cropped_image))

    return cropped_images


for image_name in os.listdir(images_path):
    if image_name.endswith('.jpg'):
        image_path = os.path.join(images_path, image_name)
        image = cv2.imread(image_path)
        label_file_name = image_name.replace('.jpg', '.txt')
        label_path = os.path.join(labels_path, label_file_name)
        
        if os.path.exists(label_path):
            with open(label_path, 'r') as file:
                labels = [line.strip().split() for line in file.readlines()]
            cropped_images = crop_image(image, labels)
        
            for i, (cls, cropped_image) in enumerate(cropped_images):
                output_file_name = f"{os.path.splitext(image_name)[0]}_crop_{i}.jpg"
                output_file_path = os.path.join(output_path, output_file_name)
                cv2.imwrite(output_file_path, cropped_image)