import os
import cv2

# Define the paths
data_path = 'cropdata'
images_path  = os.path.join(data_path, 'images')
labels_path  = os.path.join(data_path, 'labels')
output_path  = 'cropped_images'

# Create output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Function to crop image based on YOLO format labels
def crop_image(image, labels):
    h, w, _ = image.shape
    cropped_images = []
    
    for label in labels:
        cls, x_center, y_center, bbox_width, bbox_height = label
        x_center, y_center, bbox_width, bbox_height = float(x_center), float(y_center), float(bbox_width), float(bbox_height)

        # Convert from YOLO format to pixel values
        x_center *= w
        y_center *= h
        bbox_width *= w
        bbox_height *= h

        # Calculate coordinates
        x1 = int(x_center - bbox_width / 2)
        y1 = int(y_center - bbox_height / 2)
        x2 = int(x_center + bbox_width / 2)
        y2 = int(y_center + bbox_height / 2)

        # Crop image
        cropped_image = image[y1:y2, x1:x2]
        cropped_images.append((cls, cropped_image))

    return cropped_images

# Iterate over each image and label file
for image_name in os.listdir(images_path):
    if image_name.endswith('.jpg'):
        # Read image
        image_path = os.path.join(images_path, image_name)
        image = cv2.imread(image_path)
        
        # Read corresponding label file
        label_file_name = image_name.replace('.jpg', '.txt')
        label_path = os.path.join(labels_path, label_file_name)
        
        if os.path.exists(label_path):
            with open(label_path, 'r') as file:
                labels = [line.strip().split() for line in file.readlines()]
            
            # Crop image based on labels
            cropped_images = crop_image(image, labels)
            
            # Save cropped images
            for i, (cls, cropped_image) in enumerate(cropped_images):
                output_file_name = f"{os.path.splitext(image_name)[0]}_crop_{i}.jpg"
                output_file_path = os.path.join(output_path, output_file_name)
                cv2.imwrite(output_file_path, cropped_image)