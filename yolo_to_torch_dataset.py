import os
import cv2  # OpenCV for image processing
import shutil

# Directories
input_image_dir = 'logo-train/images'
input_label_dir = 'logo-train/new_labels'
output_dir = 'l_dataset/train'
classes_path = 'logo-train/classes.txt'


if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
with open(classes_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Create directories for each class
for class_name in classes:
    os.makedirs(os.path.join(output_dir, class_name), exist_ok=True)

# Process each label file
for label_file in os.listdir(input_label_dir):
    if label_file.endswith('.txt'):
        base_name = os.path.splitext(label_file)[0]
        image_file = f'{base_name}.jpg'  # or .png, depending on your image format

        # Load image
        image_path = os.path.join(input_image_dir, image_file)
        if not os.path.isfile(image_path):
            print(f"Image file not found: {image_path}")
            continue
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue

        # Read label file
        with open(os.path.join(input_label_dir, label_file), 'r') as f:
            labels = f.readlines()

        # Process each bounding box
        for label in labels:
            parts = label.strip().split()
            class_idx = int(parts[0])
            x_center, y_center, width, height = map(float, parts[1:])

            # Convert YOLO format to bounding box coordinates
            img_height, img_width = image.shape[:2]
            x_min = int((x_center - width / 2) * img_width)
            x_max = int((x_center + width / 2) * img_width)
            y_min = int((y_center - height / 2) * img_height)
            y_max = int((y_center + height / 2) * img_height)

            # Ensure crop coordinates are within image bounds
            x_min = max(x_min, 0)
            y_min = max(y_min, 0)
            x_max = min(x_max, img_width)
            y_max = min(y_max, img_height)

            # Crop the image
            cropped_image = image[y_min:y_max, x_min:x_max]

            # Check if cropped image is valid
            if cropped_image.size == 0:
                print(f"Cropped image is empty: {image_file}")
                continue

            # Determine class name and save cropped image
            class_name = classes[class_idx]
            output_path = os.path.join(output_dir, class_name, image_file)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, cropped_image)

        # Optionally, you may want to remove the original image and label files if no longer needed
        # os.remove(image_path)
        # os.remove(os.path.join(input_label_dir, label_file))