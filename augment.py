import cv2
import numpy as np
import random
import os

def get_max_image_dimensions(folder_path):
    """Get the maximum width and height of all images in the folder."""
    max_width = 0
    max_height = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            h, w, _ = image.shape
            if w > max_width:
                max_width = w
            if h > max_height:
                max_height = h
    return max_width, max_height

def rotate_image(image, angle):
    """Rotate the image by a given angle."""
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated, "_rotate"

def flip_image(image):
    """Flip the image horizontally and/or vertically."""
    flipped = cv2.flip(image, -1)
    return flipped, "_flip"

def scale_image(image, scale_factor):
    """Scale the image by a given factor."""
    (h, w) = image.shape[:2]
    scaled = cv2.resize(image, (int(w * scale_factor), int(h * scale_factor)))
    return scaled, f"_scale_{scale_factor:.2f}"

def translate_image(image, x, y):
    """Translate the image by given x and y offsets."""
    (h, w) = image.shape[:2]
    M = np.float32([[1, 0, x], [0, 1, y]])
    translated = cv2.warpAffine(image, M, (w, h))
    return translated, f"_translate_{x:.2f}_{y:.2f}"

def adjust_brightness_contrast(image, alpha, beta):
    """Adjust the brightness and contrast of the image."""
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted, f"_brightness_{alpha:.2f}_{beta}"

def blur_image(image):
    """Apply Gaussian blur to the image."""
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred, "_blur"

def add_salt_pepper_noise(image, amount):
    """Add salt-and-pepper noise to the image."""
    row, col, _ = image.shape
    s_vs_p = 0.5  # Salt vs Pepper ratio
    out = np.copy(image)

    # Salt mode
    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i-1, int(num_salt)) for i in image.shape]
    out[coords[0], coords[1], :] = 255

    # Pepper mode
    num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i-1, int(num_pepper)) for i in image.shape]
    out[coords[0], coords[1], :] = 0
    return out.astype(np.uint8), "_salt_pepper"

def hue_shift_image(image):
    """Shift the hue of the image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue_shift = random.randint(0, 50)
    hsv[:,:,0] = (hsv[:,:,0] + hue_shift) % 180
    shifted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return shifted, f"_hue_shift_{hue_shift}"

def crop_image(image):
    """Crop the image randomly."""
    h, w, _ = image.shape
    start_x = random.randint(0, w // 4)
    start_y = random.randint(0, h // 4)
    end_x = random.randint(3 * w // 4, w)
    end_y = random.randint(3 * h // 4, h)
    cropped = image[start_y:end_y, start_x:end_x]
    cropped = cv2.resize(cropped, (w, h))  # Resize to original size
    return cropped, "_crop"

def sharpen_image(image):
    """Sharpen the image."""
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened, "_sharpen"

def add_gaussian_noise(image):
    """Add Gaussian noise to the image."""
    row, col, ch = image.shape
    mean = 0
    sigma = 30  # Adjust the sigma value to make the noise more visible
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    noisy = image + gauss
    noisy = np.clip(noisy, 0, 255)  # Ensure pixel values are within [0, 255]
    return noisy.astype(np.uint8), "_gaussian_noise"

def place_image_on_background(image, background_folder):
    """Place the image onto a random background at a random position."""
    background_filename = random.choice(os.listdir(background_folder))
    background_path = os.path.join(background_folder, background_filename)
    background = cv2.imread(background_path)
    
    bg_h, bg_w, _ = background.shape
    img_h, img_w, _ = image.shape

    if img_h > bg_h or img_w > bg_w:
        #raise ValueError("The image is larger than the background.")
        return image

    # Random position for the image within the background
    x_offset = random.randint(0, bg_w - img_w)
    y_offset = random.randint(0, bg_h - img_h)

    # Place the image on the background
    combined = background.copy()
    combined[y_offset:y_offset + img_h, x_offset:x_offset + img_w] = image

    return combined

def augment_and_save_image(image, original_filename, save_folder, background_folder):
    """Apply various augmentations to an image and save each version."""
    augmented_images = []

    image = place_image_on_background(image, background_folder)

    # # Rotate
    # angle = random.uniform(-50,-30)
    # rotated_image, suffix = rotate_image(image, angle)
    # rotated_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    # cv2.imwrite(rotated_filename, rotated_image)
    # augmented_images.append(rotated_filename)

    # # Rotate
    # angle = random.uniform(30, 50)
    # rotated_image, suffix = rotate_image(image, angle)
    # rotated_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + "_2" + os.path.splitext(original_filename)[1] )
    # cv2.imwrite(rotated_filename, rotated_image)
    # augmented_images.append(rotated_filename)

    # Flip
    flipped_image, suffix = flip_image(image)
    flipped_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    cv2.imwrite(flipped_filename, flipped_image)
    augmented_images.append(flipped_filename)

    # # Scale
    # scale_factor = random.uniform(0.8, 1.2)
    # scaled_image, suffix = scale_image(image, scale_factor)
    # scaled_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    # cv2.imwrite(scaled_filename, scaled_image)
    # augmented_images.append(scaled_filename)

    # # Translate
    # x = random.uniform(-0.1, 0.1) * image.shape[1]
    # y = random.uniform(-0.1, 0.1) * image.shape[0]
    # translated_image, suffix = translate_image(image, x, y)
    # translated_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    # cv2.imwrite(translated_filename, translated_image)
    # augmented_images.append(translated_filename)

    # Adjust brightness and contrast
    alpha = random.uniform(0.8, 1.2)
    beta = random.randint(-30, 30)
    adjusted_image, suffix = adjust_brightness_contrast(image, alpha, beta)
    adjusted_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    cv2.imwrite(adjusted_filename, adjusted_image)
    augmented_images.append(adjusted_filename)

    # Blur
    blurred_image, suffix = blur_image(image)
    blurred_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    cv2.imwrite(blurred_filename, blurred_image)
    augmented_images.append(blurred_filename)

    # # Salt and pepper noise
    # noisy_image, suffix = add_salt_pepper_noise(image, 0.05)
    # noisy_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    # cv2.imwrite(noisy_filename, noisy_image)
    # augmented_images.append(noisy_filename)

    # Hue shift
    # hue_shifted_image, suffix = hue_shift_image(image)
    # hue_shifted_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    # cv2.imwrite(hue_shifted_filename, hue_shifted_image)
    # augmented_images.append(hue_shifted_filename)

    # # Crop
    # cropped_image, suffix = crop_image(image)
    # cropped_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    # cv2.imwrite(cropped_filename, cropped_image)
    # augmented_images.append(cropped_filename)

    # Sharpen
    sharpened_image, suffix = sharpen_image(image)
    sharpened_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    cv2.imwrite(sharpened_filename, sharpened_image)
    augmented_images.append(sharpened_filename)

    # Gaussian noise
    # gaussian_noisy_image, suffix = add_gaussian_noise(image)
    # gaussian_noisy_filename = os.path.join(save_folder, os.path.splitext(original_filename)[0] + suffix + os.path.splitext(original_filename)[1])
    # cv2.imwrite(gaussian_noisy_filename, gaussian_noisy_image)
    # augmented_images.append(gaussian_noisy_filename)

    return augmented_images

def augment_images_in_folder(folder_path, background_folder):
    """Apply augmentations to all images in a folder and save the augmented images."""
    background_files = os.listdir(background_folder)
    max_width, max_height = get_max_image_dimensions(folder_path)
    if len(background_files) < len(os.listdir(folder_path)*5):
            for i in range(len(os.listdir(folder_path))*5 - len(background_files)):
                random_bg = cv2.randn(np.zeros((max_height+100, max_width+100, 3), np.uint8), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (50, 50, 50))
                random_bg_filename = f"background_{i}.jpg"
                cv2.imwrite(os.path.join(background_folder, random_bg_filename), random_bg)
            background_files = os.listdir(background_folder)
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)

            save_folder = folder_path  # Save augmented images in the same folder
            augmented_image_paths = augment_and_save_image(image, filename, save_folder, background_folder)

            print(f"Augmented and saved images for {filename}:")
            for img_path in augmented_image_paths:
                print(img_path)

# Example usage
folder_path = 'augmentinput'
# folder_path = 'background'
background_folder = 'background'
augment_images_in_folder(folder_path, background_folder)

